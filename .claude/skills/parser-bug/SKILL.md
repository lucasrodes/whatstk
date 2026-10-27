---
name: parser-bug
description: Investigate and fix a whatstk parsing bug, security report or CVE. Use when a chat fails to parse, parses into wrong/missing rows, when auto-header detection picks the wrong format, when emoji or unicode are mangled, or when triaging a vulnerability report against the parser.
---

# Fixing a parser bug

Parsing correctness is whatstk's product. The existing test suite will **not** catch a real-world
parsing bug on its own (see "the circularity trap" below), so the discipline here is: reproduce
first, localise the layer, write a failing test, then fix.

## Step 1 — Reproduce with a minimal input

Get the smallest chat snippet that shows the problem. Never commit a user's real export — redact
message bodies and rename users, keeping the **header structure byte-identical** (that is where the
bug lives). Watch for invisible characters: narrow no-break space (U+202F), LRM/RLM marks and
zero-width joiners are common in real exports and are routinely lost in copy-paste.

```bash
# Inspect the raw bytes of the first lines — invisible characters show up here
head -c 400 chat.txt | python3 -c "import sys; print(sys.stdin.buffer.read() if 0 else open(0,'rb').read()[:400])"
```

Confirm whether the report is about automatic detection or an explicitly passed `hformat`; they fail
for different reasons.

## Step 2 — Localise the layer

`df_from_whatsapp` is a pipeline. Bisect it rather than guessing:

```python
from whatstk.whatsapp.parser import (
    _str_from_file, _clean_text, generate_regex, _parse_chat, _remove_alerts_from_df,
)
from whatstk.whatsapp.auto_header import extract_header_from_text
import re

path = "chat.txt"

# 1. Read
text = _str_from_file(path)
print("read:", len(text), "chars")

# 2. Clean  (NFKD normalisation + stripping of invisible characters)
cleaned = _clean_text(text)
print("cleaning changed the text:", cleaned != text)

# 3. Infer the header format
hformat = extract_header_from_text(cleaned)
print("inferred hformat:", repr(hformat))      # None => detection failed

# 4. hformat -> regex
r, r_x = generate_regex(hformat)
print("matches found:", len(list(re.finditer(r, cleaned))))   # 0 => regex/format mismatch

# 5. Parse
df = _parse_chat(cleaned, r)
print(df.head().to_string())
print("rows:", len(df))

# 6. Alert stripping — a frequent cause of truncated messages
df2 = _remove_alerts_from_df(r_x, df)
print("messages altered by alert-stripping:", (df2["message"] != df["message"]).sum())
```

Map the symptom to the layer:

| Symptom | Likely layer | File |
| ------- | ------------ | ---- |
| `RuntimeError: Header automatic extraction failed` | inference returned `None` | `auto_header.py` |
| Parses, but day and month are swapped | day-position heuristic | `auto_header.py` |
| `HFormatError` / 0 regex matches | code→regex mapping | `parser.py: generate_regex` |
| Messages merged, or multi-line messages lost | message boundaries | `parser.py: _get_message` |
| Message text truncated | alert stripping | `parser.py: _remove_alerts_from_line` |
| Emoji broken, odd spacing, mangled accents | unicode normalisation | `parser.py: _clean_text` |
| Wrong hour on 12h chats | AM/PM handling | `parser.py: _parse_line` |
| Rows missing after merging exports | merge semantics | `utils/chat_merge.py` |

Two known traps worth checking before digging further:

- **Day/month swap on short chats.** The day is located by looking for a value between 28 and 31. A
  chat that never reaches day 28 gives nothing to match and position 0 is chosen by default, so
  `%y-%m-%d` is inferred as `%d-%y-%m`. Issue
  [#175](https://github.com/lucasrodes/whatstk/issues/175).
- **Emoji damage.** `_clean_text` applies NFKD and strips U+200D (ZWJ), which decomposes
  multi-codepoint emoji sequences. Issues
  [#171](https://github.com/lucasrodes/whatstk/issues/171) /
  [#172](https://github.com/lucasrodes/whatstk/issues/172), draft PR #173 — coordinate there instead
  of patching separately.

## Step 3 — Write the failing test first

### ⚠ The circularity trap

`tests/whatsapp/test_parser.py::test_df_from_whatsapp` parses chats that **whatstk's own generator**
produced from the same `header_format_support.json` the parser reads. It proves self-consistency,
not real-world correctness, and it will happily stay green while the bug you are fixing is live.

**A green suite is not evidence your fix works.** Add a test built from the real-world snippet,
written inline so it does not depend on generated fixtures:

```python
def test_parses_ios_12h_header(tmp_path):
    """Regression for #NNN: <one line on what was reported>."""
    chat = tmp_path / "chat.txt"
    chat.write_text(
        "[12/08/2016, 4:20:11 PM] Ash Ketchum: Hey guys!\n"
        "[12/08/2016, 4:21:03 PM] Misty: Hi!\n",
        encoding="utf-8",
    )
    df = df_from_whatsapp(str(chat))
    assert len(df) == 2
    assert df.loc[0, "username"] == "Ash Ketchum"
    assert df.loc[0, "date"].hour == 16      # 12h -> 24h conversion
```

Substitute the reported snippet for the body above; the one shown parses correctly today and is only
a shape to copy. Run the test and confirm it fails **for the reported reason** before writing any
fix — one that fails for an unrelated reason (a typo'd fixture, a missing `tests/chats/`) proves
nothing.

Two assertions are worth adding whenever relevant, because they catch the most common silent
corruptions: the exact row **count** (messages merged or dropped), and the **full text** of a message
containing emoji or a newline (unicode damage, truncation).

## Step 4 — Fix at the right layer

Keep the change as narrow as the bug. Specifically:

- Adding a new header layout means adding it to `whatstk/whatsapp/assets/header_format_support.json`
  with the right `auto_header` flag — and regenerating fixtures with `make generate-test-data`, since
  that file drives the generator too.
- Changing `_clean_text` affects **every** chat. Prefer narrowing the transformation (for example,
  applying it to headers only) over broadening it.
- Changing `generate_regex` affects all 96 formats at once. Check the capture-group names still match
  what `_parse_line` reads.

## Step 5 — Verify

```bash
make unittest                       # the regression test plus the full suite
make generate-test-data             # if you touched the format catalogue or the generator
make test                           # format, lint, typecheck too
```

Then confirm you did not regress the other formats — this is the check the normal suite is weakest at:

```python
from whatstk.whatsapp.hformat import get_supported_hformats_as_dict
from whatstk.whatsapp.auto_header import extract_header_from_text
from whatstk.whatsapp.parser import df_from_whatsapp
from whatstk.utils.utils import _map_hformat_filename
from tests.paths import TEST_CHATS_HFORMATS_DIR

# extract_header_from_text returns brackets pre-escaped (\[ \]); the catalogue stores them raw.
unescape = lambda h: h.replace(r"\[", "[").replace(r"\]", "]") if h else h

bad = []
for e in get_supported_hformats_as_dict():
    f = TEST_CHATS_HFORMATS_DIR / f"{_map_hformat_filename(e['format'])}.txt"
    inferred = extract_header_from_text(f.read_text(encoding="utf-8"))
    manual = df_from_whatsapp(str(f), hformat=e["format"])
    auto = df_from_whatsapp(str(f))
    if unescape(inferred) != e["format"] or not manual.equals(auto):
        bad.append((e["format"], inferred))
print("mismatches:", bad or "none")   # expect: none
```

A clean run reports `none` across all 96 formats. If you see 48 mismatches that differ only by
backslashes, you dropped the `unescape` call.

## Step 6 — Ship it

Branch from `develop`, PR back into `develop` (never `main`). Reference the issue number, and state
in the PR description **how the fix was verified against a real export** rather than only against
generated fixtures.

---

## Triaging a security report or CVE

Reports against whatstk usually concern untrusted input: a crafted `.txt` or `.zip`, or a URL.
Establish exploitability before writing a fix — automated scanners produce a high false-positive rate
on this codebase.

**Verified non-issues** (confirm again if the report disagrees, but these are the usual noise):

- **Zip Slip / path traversal in `_str_from_file`.** The code calls `ZipFile.extractall()` into a
  `TemporaryDirectory`. CPython's `extractall` has sanitised member paths since 2.7.4 — a
  `../../../x.txt` entry is written *inside* the destination, not outside. Verify before accepting:

  ```python
  import zipfile, tempfile, os, pathlib
  with zipfile.ZipFile('evil.zip','w') as z:
      z.writestr('../../../../tmp/PWNED.txt', 'owned')
  with tempfile.TemporaryDirectory() as d:
      zipfile.ZipFile('evil.zip').extractall(d)
      print([str(p) for p in pathlib.Path(d).rglob('*') if p.is_file()])
  print('escaped:', os.path.exists('/tmp/PWNED.txt'))   # expect False
  ```

**Worth taking seriously:**

- **Decompression bombs.** Fixed in 0.9.0: the zip member is read bounded and in memory, and
  `max_size` (50 MB default) caps every source. A new report here must show how it gets past
  `max_size`. Note parsing still peaks at ~13x the text — bounded, not cheap (issue #186).
- **Catastrophic regex backtracking.** Fixed in 0.9.0 by passing hformat literals through
  `re.escape`. The regex is still built per file and run across the whole text, and
  `_remove_alerts_from_line` runs `re.search` once per message. Time any suspected input against a
  known-good baseline rather than reasoning about it.
- **URL fetching.** `_str_from_file` calls `urlopen` on anything starting with `http`. Consider what
  an attacker-supplied path reaches in a server-side deployment. Google Drive loading was removed in
  0.10.0, so `gdrive://` paths now raise `ValueError` instead of reaching the network.

Confirm the affected version and the exact entry point, reproduce it, then follow the normal flow
above: failing test, narrow fix, PR to `develop`. Coordinate disclosure through
[`SECURITY.md`](../../../SECURITY.md) — fixes for confirmed vulnerabilities ship as a patch release
(use the `release` skill) and are credited in a GitHub Security Advisory.
