# AGENTS.md

Guidance for AI coding agents (and new human contributors) working on **whatstk**.

## What this project is

whatstk parses WhatsApp chat exports into pandas DataFrames. A maintained personal project since
2016, ~1.5k PyPI downloads/month, GPL-3.0, Python 3.11+.

**Strategic direction:** double down on being *the* reliable WhatsApp parser. Parsing correctness is
the product. The plotting (`whatstk.graph`), Google Drive (`whatstk.utils.gdrive`) and chat generation
(`whatstk.whatsapp.generation`) modules are legacy scope that is being slimmed down — do not invest in
them or expand their surface area without being asked. See issue
[#177](https://github.com/lucasrodes/whatstk/issues/177).

When a change trades parser correctness against anything else, correctness wins.

## Quick reference

```bash
make .venv              # create/refresh the environment — START HERE
make generate-test-data # generate test fixtures (required before tests can run)
make test               # format + lint + typecheck + unit tests (what CI runs)

make check.format       # ruff format --check
make format             # ruff format (apply)
make check.lint         # ruff check
make check.type         # pyright
make unittest           # pytest with coverage
make unittest-parallel   # same, via pytest-xdist

make docs               # build Sphinx docs to docs/_build/html
make docs.serve         # build and serve on :8000
make help               # list all targets
```

Always run commands through `uv run` / `make`; never invoke a bare `python` or `pip`.

## Repository map

```
whatstk/
├── __init__.py             Public API: WhatsAppChat, df_from_whatsapp, FigureBuilder
├── _chat.py                BaseChat — platform-agnostic chat object (df, users, merge, filter_dates…)
├── data.py                 URLs of sample chats hosted in this repo
├── whatsapp/
│   ├── parser.py           ★ CORE. Text → DataFrame. hformat → regex, message extraction
│   ├── auto_header.py      ★ CORE. Infers the hformat from the chat text
│   ├── objects.py          WhatsAppChat (BaseChat subclass), from_source/from_sources, to_txt/to_zip
│   ├── hformat.py          Queries the supported-format catalogue
│   └── assets/header_format_support.json   96 supported header formats
├── analysis/               get_interventions_count, get_response_matrix
├── graph/                  FigureBuilder + plotly figures (legacy scope)
├── utils/                  chat_merge, gdrive (legacy scope), exceptions, COLNAMES_DF
└── scripts/                CLI entry points: whatstk-to-csv, whatstk-graph, whatstk-generate-chat
```

The library is small (~2.7k LOC across 30 files). Read `parser.py` and `auto_header.py` before changing anything in
the parsing path.

### The output schema

Every loader returns a DataFrame with a **RangeIndex** and three columns, named via
`whatstk.utils.utils.COLNAMES_DF`:

| column     | dtype            |
| ---------- | ---------------- |
| `date`     | `datetime64[ns]` |
| `username` | `string`         |
| `message`  | `string`         |

A fourth column, `message_type` (`'user'` / `'system'`), appears only when `message_type=True` is
passed. That flag is **experimental** and emits a `FutureWarning`. Use the `COLNAMES_DF` constants
rather than hardcoding column-name strings.

## The header format (`hformat`) model

This is the central domain concept. Every WhatsApp message line begins with a header encoding
timestamp and sender; its layout varies by device, OS and locale:

```
06.08.2016, 13:23 - Ash Ketchum: Hey guys!
└──────── header ──────────────┘ └ message ┘
```

That header is described by an `hformat` string — here `'%d.%m.%y, %H:%M - %name:'` — using the codes
`%y`/`%Y`, `%m`, `%d`, `%H` (24h), `%I` (12h), `%p`/`%P` (AM/PM), `%M`, `%S` and `%name`.

The flow is: **hformat → regex → parse**.

1. `generate_regex()` in `parser.py` substitutes each code for a named capture group via the
   `regex_simplifier` dict.
2. `_parse_chat()` runs `re.finditer` over the whole text. Each match is a header; a message is
   everything between the end of one header and the start of the next, which is how multi-line
   messages work.
3. If no `hformat` is given, `auto_header.extract_header_from_text()` infers it first.

`whatsapp/assets/header_format_support.json` is the catalogue of the 96 formats whatstk claims to
support. It is **packaged data** and drives both the generator and the test suite — see below.

### Known weakness in auto-detection

`_extract_header_format_from_components()` locates the day by looking for a position whose maximum
value falls between 28 and 31. On a chat that never reaches day 28, no position qualifies and
`idxmax()` silently returns position 0. A short `%y-%m-%d` chat is then inferred as `%d-%y-%m`, and a
short `%m/%d/%y` chat as `%d/%m/%y` — day and month swapped, no error raised. Tracked in issue
[#175](https://github.com/lucasrodes/whatstk/issues/175). Do not assume auto-detection is correct when
debugging a parsing report; check the inferred format explicitly.

## Testing

```bash
make generate-test-data   # must run once before the first test run
make unittest
```

`tests/chats/` is **generated, not committed** (it is gitignored). `make generate-test-data` invokes
`whatstk-generate-chat`, which writes ~192 files: one `.txt` and one `.zip` per supported hformat,
plus two chats under `tests/chats/merge/` for merge tests. `make unittest` regenerates them
automatically if the directory is missing.

### ⚠ The parser test suite is circular

`tests/whatsapp/test_parser.py::test_df_from_whatsapp` iterates over
`header_format_support.json`, loads the chat that **whatstk's own generator** wrote in that format,
and asserts the parse round-trips and that all formats yield identical DataFrames.

This validates self-consistency, **not** real-world correctness. The generator and the parser share
the same format catalogue, so a format that WhatsApp actually emits differently will pass the suite
while failing on real exports. The only non-generated fixture is the hand-written
`chats/whatsapp/pokemon.txt`.

**Therefore: a parser bug fix is not proven by the existing suite passing.** Always add a regression
test built from a real-world snippet. Building a real-export fixture corpus is issue
[#174](https://github.com/lucasrodes/whatstk/issues/174).

### Other notes

- Coverage must stay ≥80% (`.coveragerc`), currently ~97%.
- `tests/paths.py` holds the fixture path constants — use them, don't rebuild paths.
- `test_df_from_whatsapp_url` hits the network and is marked `@pytest.mark.flaky`.
- Mock the `gdrive` path (`pydrive2`) rather than authenticating; see `test_parser.py`.

## Branching and releases

The project follows **git-flow**:

```
feature/xyz ──PR──► develop ──► release/X.Y.Z ──PR──► main ──► GitHub Release ──► PyPI
```

- **`develop`** is the integration branch and the **default target for all PRs**. Work accumulates
  here until it is worth releasing.
- **`main`** reflects the latest release. Only release branches merge into it.
- **`release/X.Y.Z`** is cut from `develop` when a release is ready; the version bump happens there.
- After a release, merge `main` back into `develop` so the two do not drift. They should be identical
  immediately after a release.

Never commit directly to `main` or `develop`; never bump the version outside a release branch.

Releasing is a multi-step procedure with ordering constraints — **use the `release` skill**
(`.claude/skills/release/SKILL.md`) rather than improvising.

### CI

- `ci-quick.yml` — every push and draft PR: Ubuntu / Python 3.13, full check suite.
- `ci-full.yml` — PRs to `main`/`develop` and pushes there: 3 OSes × Python 3.11–3.14.
- `release.yml` — on a **published GitHub Release**: full matrix, then PyPI trusted publishing.

Read the Docs builds independently via its own webhook; no workflow triggers it.

## Conventions

- **Formatting/linting:** ruff, line length 120, double quotes. Enabled rule sets include `D`
  (pydocstyle, google convention), `ANN` (type annotations), `S` (bandit), `B`, `A`, `C90`
  (complexity ≤10). Public functions therefore **need both a docstring and type annotations**; tests
  are exempt (see `per-file-ignores`).
- **Docstrings:** Google style with `Args:` / `Returns:` / `Raises:`. They are rendered by Sphinx, so
  reStructuredText directives (`..  code-block:: python`, `:func:`…``) are used inside them. A
  malformed docstring becomes a docs-build warning — run `make docs` after touching one.
- **Commit messages:** short, lowercase, imperative ("fix rtd build"). Issues and PR titles use
  conventional-commit prefixes (`feat:`, `fix:`, `chore:`).
- **Typing:** `from typing import Optional, List, Dict, Tuple` style is used throughout; match the
  surrounding file rather than modernising it piecemeal.
- Prefix internal helpers with `_`. Only names in `whatstk/__init__.py::__all__` are public API.

## Gotchas

These will each cost you a debugging cycle:

1. **`make .venv`, not `make install.dev`.** `.venv` runs `uv sync --all-extras` and is what CI uses.
   `install.dev` runs a bare `uv pip install -e .[dev]`, which does not create an environment and
   installs into whatever interpreter `uv` happens to discover.
2. **Bump versions only via `make bump.patch|minor|major`.** A raw `bump-my-version bump patch`
   yields `0.8.2.dev0`, not `0.8.2`, because of the optional `pre` part in the serialize config. The
   make targets compute the version explicitly to avoid this.
3. **`.coveragerc` wins over `pyproject.toml`.** Coverage reads `.coveragerc` when present, so
   `[tool.coverage.*]` in `pyproject.toml` is dead configuration. Edit `.coveragerc`.
4. **`make check.type` is real now, but not complete.** `pyrightconfig.json` runs in `standard`
   mode with 20 previously-disabled checks back on. Seven remain off, each because the pandas and
   plotly stubs make them noise rather than signal (`reportReturnType`, `reportArgumentType`,
   `reportAttributeAccessIssue`, `reportCallIssue`, `reportUnhashable`, `reportMissingTypeStubs`,
   `reportUnusedFunction`). **Also run `uvx ty check whatstk`** — `ty` found every annotation bug
   fixed in 0.9.0, including ones pyright still cannot see. Remaining work: issue
   [#177](https://github.com/lucasrodes/whatstk/issues/177).
5. **`whatstk/data.py` sample-chat URLs point at the `develop` branch.** Chats added under `chats/`
   are only reachable once they land on `develop`.
6. **The version string lives in four files** — `pyproject.toml` (twice), `whatstk/__init__.py`,
   `docs/conf.py`, `README.md` — all kept in sync by bump-my-version. Never edit them by hand.
7. **`_clean_text()` currently normalises with NFKD and strips ZWJ**, which breaks multi-codepoint
   emoji sequences. Changing it is the subject of issues
   [#171](https://github.com/lucasrodes/whatstk/issues/171) /
   [#172](https://github.com/lucasrodes/whatstk/issues/172) and draft PR #173 — coordinate there
   rather than patching independently.
8. **`merge_chats()` returns the deduplicated union, not a concatenation.** Two messages are the
   same only when date, username and text all match, so the same message with different timestamps
   in two exports is kept twice. Repeats are numbered per chat before deduplicating, which is what
   separates "sent twice" from "exported twice" — preserve that if you touch it.
9. **Input is size-capped by default.** `df_from_whatsapp(max_size=...)` refuses text over 50 MB
   (`MAX_INPUT_SIZE`). Parsing peaks at ~13x the text, so the cap is about memory, not disk. Pass
   `max_size=None` in any test or tool that deliberately handles a huge chat.

## Documentation

Sphinx sources live in `docs/`, published to
[whatstk.readthedocs.io](https://whatstk.readthedocs.io/en/latest/).

- `docs/index.rst` — root toctree.
- `docs/source/getting_started/` — task-oriented guides.
- `docs/source/code_examples/` — worked examples (several are `.. include::`-ed into getting_started).
- `docs/source/api/` — the API reference. **This is the only apidoc tree**; a duplicate auto-generated
  set at `docs/source/whatstk*.rst` was removed, do not regenerate it with `sphinx-apidoc`.
- `docs/llms.txt` — a condensed map of the library for AI assistants, served at the docs root via
  `html_extra_path`. **Review it whenever you change the public API, the output schema, the header
  format model, or the known limitations.** It is hand-written, not generated, so nothing will tell
  you it has gone stale. A substantial change that leaves `llms.txt` describing the old behaviour is
  worse than no `llms.txt`, because assistants will confidently emit code against it.

`make docs` currently builds with 15 warnings, all from `index.rst` doing
`.. include:: source/about.rst` (which makes `autosectionlabel` see every label twice). **Do not
introduce new warnings**; check the count before and after your change.

Doc examples are the main thing LLMs learn from, so every snippet should run as written. Verify
before committing.

## Where to look next

Current roadmap, as GitHub issues:

| Issue | Topic |
| ----- | ----- |
| [#174](https://github.com/lucasrodes/whatstk/issues/174) | Real-export fixture corpus (fixes the circular tests) |
| [#175](https://github.com/lucasrodes/whatstk/issues/175) | Auto-header detection robustness |
| [#176](https://github.com/lucasrodes/whatstk/issues/176) | Message-type classification (media/edited/deleted/poll) |
| [#177](https://github.com/lucasrodes/whatstk/issues/177) | Slim the package, tighten correctness |
| [#178](https://github.com/lucasrodes/whatstk/issues/178) | AI-friendliness (llms.txt, AGENTS.md, MCP server) |

## Skills

| Skill | Use when |
| ----- | -------- |
| `release` | Cutting and publishing a release |
| `parser-bug` | Investigating a parsing bug, CVE report or incorrect-output issue |
