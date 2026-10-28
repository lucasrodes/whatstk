"""Check that `pip install whatstk`, with no extras, is enough to parse a chat.

Run by the `lean-install` CI job against a venv holding only the built wheel and its required
dependencies. It is deliberately not a pytest module: pytest is not installed in that venv, and the
filename keeps it out of collection during a normal test run.

Invoke directly: `python tests/lean_install_check.py`. Exits non-zero on the first failure.
"""

import os
import sys
import tempfile
import warnings


CHAT = "\n".join(f"0{d}.08.2016, 13:2{d} - {'Ash Ketchum' if d % 2 else 'Misty'}: message {d}" for d in range(1, 7))

FORBIDDEN = ["plotly", "seaborn", "scipy", "pydrive2", "lorem"]


def ok(message: str) -> None:
    print(f"  ok    {message}")


def main() -> int:
    warnings.simplefilter("ignore")

    import whatstk

    ok(f"import whatstk ({whatstk.__version__})")

    # The point of the [viz] extra: importing the library must not drag plotting in.
    leaked = [name for name in ("plotly", "seaborn") if name in sys.modules]
    assert not leaked, f"importing whatstk pulled in {leaked}"
    ok("importing whatstk does not import plotly or seaborn")

    import importlib.util

    present = [name for name in FORBIDDEN if importlib.util.find_spec(name) is not None]
    assert not present, f"a base install should not have {present}"
    ok(f"none of {', '.join(FORBIDDEN)} is installed")

    from whatstk import WhatsAppChat, df_from_whatsapp

    path = os.path.join(tempfile.mkdtemp(), "chat.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(CHAT)

    df = df_from_whatsapp(path)
    assert len(df) == 6, f"expected 6 messages, got {len(df)}"
    assert list(df.columns) == ["date", "username", "message"], list(df.columns)
    ok(f"df_from_whatsapp parses {len(df)} messages into {list(df.columns)}")

    chat = WhatsAppChat.from_source(path)
    assert chat.users == ["Ash Ketchum", "Misty"], chat.users
    ok("WhatsAppChat.from_source works")

    from whatstk.analysis import get_interventions_count

    get_interventions_count(chat=chat, date_mode="date", msg_length=False)
    ok("whatstk.analysis works without the viz extra")

    # Removed in 0.10.0 -- the path has to say so rather than fail as a missing file.
    try:
        df_from_whatsapp("gdrive://some-file-id")
    except ValueError as err:
        assert "0.10.0" in str(err), str(err)
        ok("a gdrive:// path explains that support was removed")
    else:
        raise AssertionError("gdrive:// path did not raise")

    # Reaching for plotting without the extra has to name the extra, not raise ModuleNotFoundError.
    try:
        _ = whatstk.FigureBuilder
    except ImportError as err:
        assert "whatstk[viz]" in str(err), str(err)
        ok("FigureBuilder raises an ImportError naming whatstk[viz]")
    else:
        raise AssertionError("FigureBuilder resolved without plotly installed")

    print("\nBase install is self-sufficient for parsing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
