from datetime import datetime

import pandas as pd
import pytest

from whatstk.utils.utils import _map_hformat_filename
from whatstk.whatsapp.auto_header import (
    extract_header_from_text,
    _extract_elements_template_from_lines,
    _score_date_order,
)
from whatstk.whatsapp.generation import ChatGenerator
from whatstk.whatsapp.hformat import get_supported_hformats_as_list
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


def test_outlier_first_line_does_not_decide_the_format(tmp_path):
    """The majority shape must win, not whichever valid header happens to come first.

    The outlier filter builds `template_list_`, but the template was then read from the unfiltered
    `template_list`. A first line whose numeric signature differs from the rest therefore chose the
    format for the whole chat, producing a malformed hformat with two %name groups and a raw
    re.PatternError rather than an HFormatError.
    """
    chat = tmp_path / "chat.txt"
    chat.write_text(
        "\n".join(
            ["15.04.2016, 15:04:33 - Pokemon Chat: encrypted notice"]  # has seconds
            + [f"0{d}.08.2016, 13:2{d} - Ash: msg {d}" for d in range(1, 7)]  # the other six do not
        ),
        encoding="utf-8",
    )
    text = chat.read_text(encoding="utf-8")

    assert extract_header_from_text(text) == "%d.%m.%y, %H:%M - %name:"

    # The six majority-format messages parse. The odd line out cannot, since no single hformat
    # matches both shapes -- but that is a dropped outlier, not a crash on the whole file.
    df = df_from_whatsapp(str(chat))
    assert len(df) == 6
    assert set(df["username"]) == {"Ash"}


# --- #175 bug 1: day/year inference on chats that never reach day 28 ---------------------------

SPANS = [
    ("two days", datetime(2016, 8, 2, 12, 0), 8),
    ("one week", datetime(2016, 8, 7, 12, 0), 15),
    ("three weeks", datetime(2016, 8, 20, 12, 0), 40),
    ("one year", datetime(2016, 12, 28, 12, 0), 150),
]


@pytest.mark.parametrize("label, last, size", SPANS, ids=[s[0] for s in SPANS])
def test_detection_does_not_depend_on_the_chat_spanning_day_28(label, last, size, tmp_path):
    """Every supported format must be detected regardless of how long the chat runs.

    The day used to be located by looking for a value between 28 and 31. On a chat that never
    reaches day 28 nothing matched and the lookup silently fell back to the first position, so
    72 of the 96 formats were mis-detected — either producing wrong dates with no error, or an
    uncaught ValueError from datetime.
    """
    chat = ChatGenerator(size=size, seed=3).generate(last_timestamp=last)

    wrong = []
    for hformat in get_supported_hformats_as_list():
        path = tmp_path / f"{_map_hformat_filename(hformat)}.txt"
        chat.to_txt(str(path), hformat=hformat)
        if extract_header_from_text(path.read_text(encoding="utf-8")) != hformat:
            wrong.append(hformat)

    assert wrong == []


def test_short_chat_dates_match_the_explicit_hformat(tmp_path):
    """Detection has to agree with the format the chat was actually written in, date for date."""
    chat = ChatGenerator(size=25, seed=11).generate(last_timestamp=datetime(2016, 8, 12, 12, 0))

    for hformat in ["%y-%m-%d, %H:%M - %name:", "%m/%d/%y, %H:%M - %name:", "%d.%m.%y, %H:%M - %name:"]:
        path = tmp_path / f"{_map_hformat_filename(hformat)}.txt"
        chat.to_txt(str(path), hformat=hformat)
        explicit = df_from_whatsapp(str(path), hformat=hformat)
        detected = df_from_whatsapp(str(path))
        assert detected["date"].equals(explicit["date"]), hformat


def test_impossible_component_values_are_rejected():
    """A month above 12 or a day above 31 rules an ordering out entirely."""
    df = pd.DataFrame({0: [2016, 2016], 1: [8, 9], 2: [15, 16]})

    assert _score_date_order(df, day_pos=2, month_pos=1, year_pos=0) is not None
    assert _score_date_order(df, day_pos=0, month_pos=1, year_pos=2) is None  # day 2016
    assert _score_date_order(df, day_pos=1, month_pos=2, year_pos=0) is None  # month 15


def test_falls_back_when_no_ordering_fits():
    """If every ordering is impossible, fall back rather than refuse to parse.

    Reachable with components that cannot be a date at all — here every column exceeds 31, so no
    assignment of day/month/year is valid.
    """
    from whatstk.whatsapp.auto_header import _infer_date_positions

    df = pd.DataFrame({0: [99, 98], 1: [97, 96], 2: [95, 94], 3: [10, 11], 4: [30, 31]})

    day_pos, month_pos, year_pos = _infer_date_positions(df)

    assert sorted([day_pos, month_pos, year_pos]) == [0, 1, 2]
