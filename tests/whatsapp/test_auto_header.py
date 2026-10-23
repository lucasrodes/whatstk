import pytest

from whatstk.whatsapp.auto_header import extract_header_from_text, _extract_elements_template_from_lines
from whatstk.whatsapp.parser import df_from_whatsapp


def test_extract_header_from_text():
    _ = extract_header_from_text("bla bla bla")
    assert _ is None


@pytest.mark.parametrize(
    "line, expected",
    [
        ("06.08.2016, 13:23 - Ash Ketchum: Hey guys!", "%d.%m.%y, %H:%M - %name:"),
        ("[06.08.2016 13:23] Ash Ketchum: Hey guys!", "[%d.%m.%y %H:%M] %name:"),
    ],
)
def test_extract_header_returns_a_usable_hformat(line, expected, tmp_path):
    r"""The detected format must be a plain hformat that can be passed straight back to the parser.

    Regression: bracketed (iOS-style) headers were returned pre-escaped as ``\\[...\\]``. Feeding that
    back in as ``hformat`` escaped it a second time and raised a raw ``re.PatternError``.
    """
    text = "\n".join(line.replace("06.08.2016", f"0{d}.08.2016") for d in range(1, 6))
    chat = tmp_path / "chat.txt"
    chat.write_text(text, encoding="utf-8")

    hformat = extract_header_from_text(text)
    assert hformat == expected

    # Detected format round-trips, and gives the same result as auto-detection.
    assert df_from_whatsapp(str(chat), hformat=hformat).equals(df_from_whatsapp(str(chat)))


def test_extract_elements_template_from_lines():
    elements_list, template_list = _extract_elements_template_from_lines(["testing"])
    assert elements_list == []
    assert template_list == []
