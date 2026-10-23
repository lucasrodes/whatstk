import itertools

from tests.paths import TEST_CHATS_MERGE_DIR
import pandas as pd
import pytest
from whatstk.utils.chat_merge import merge_chats
from whatstk.whatsapp.parser import df_from_whatsapp


filename1 = str(TEST_CHATS_MERGE_DIR / "file1.txt")
filename2 = str(TEST_CHATS_MERGE_DIR / "file2.txt")


def _chat(start, end, tag) -> pd.DataFrame:
    """Build a chat covering a date range, one message per day."""
    dates = pd.date_range(start, end, freq="D")
    return pd.DataFrame(
        {
            "date": dates,
            "username": [tag] * len(dates),
            "message": [f"{tag} message {i}" for i in range(len(dates))],
        }
    )


def test_merge_two_chats():
    df1 = df_from_whatsapp(filename1)
    df2 = df_from_whatsapp(filename2)
    df = merge_chats([df1, df2])
    assert isinstance(df, pd.DataFrame)
    # Order of the inputs must not change the result.
    assert df.equals(merge_chats([df2, df1]))
    # Two non-overlapping exports of different chats keep every message.
    assert len(df) == len(df1) + len(df2)


# Three non-overlapping chats, deliberately not in chronological order.
CHATS = {
    "oldest": _chat("2020-01-01", "2020-06-30", "oldest"),
    "middle": _chat("2020-07-01", "2020-12-31", "middle"),
    "newest": _chat("2021-01-01", "2021-12-31", "newest"),
}
EXPECTED_ROWS = sum(len(df) for df in CHATS.values())


@pytest.mark.parametrize("order", list(itertools.permutations(CHATS)))
def test_merge_chats_keeps_all_messages_regardless_of_input_order(order):
    """Merging must not depend on the order the chats are passed in.

    Regression: chats were sorted by ``df.index.min()``, but parsed chats carry a RangeIndex, so
    every chat sorted equal and the input order was preserved. Merging pairwise in a non-chronological
    order silently dropped whole chats.
    """
    df = merge_chats([CHATS[name] for name in order])

    assert len(df) == EXPECTED_ROWS
    assert set(df["username"]) == set(CHATS)
    assert df["date"].is_monotonic_increasing


# --- Report #1872: merging must not discard messages that overlap in time ----------------------


def test_merge_keeps_messages_inside_an_overlapping_range():
    """Two exports of the same chat taken at different times both carry unique messages.

    Report #1872: merging kept the earlier chat whole and appended only messages strictly newer
    than its last one, so anything the later export added *inside* the covered range was dropped.
    """
    early = _chat("2021-01-01", "2021-01-10", "early")
    late = _chat("2021-01-05", "2021-01-15", "late")

    df = merge_chats([early, late])

    assert len(df) == len(early) + len(late)
    assert df["date"].is_monotonic_increasing


def test_merge_deduplicates_the_same_message_across_chats():
    """The same conversation exported twice must not double every message."""
    chat = _chat("2021-01-01", "2021-01-05", "same")

    assert len(merge_chats([chat, chat.copy()])) == len(chat)


def test_merge_keeps_a_genuinely_repeated_message():
    """Deduplication must not collapse a message a user really did send twice."""
    twice = pd.DataFrame(
        {
            "date": pd.to_datetime(["2021-01-01 10:00", "2021-01-01 10:00"]),
            "username": ["Ash", "Ash"],
            "message": ["ok", "ok"],
        }
    )
    # Both survive on their own...
    assert len(merge_chats([twice])) == 2
    # ...and the pair is not multiplied when the same chat is exported twice.
    assert len(merge_chats([twice, twice.copy()])) == 2


def test_merge_handles_frames_without_a_username_column():
    """System-message frames carry no username, so the identity key must adapt."""
    a = pd.DataFrame({"date": pd.to_datetime(["2021-01-01"]), "message": ["created"]})
    b = pd.DataFrame({"date": pd.to_datetime(["2021-01-02"]), "message": ["encrypted"]})

    df = merge_chats([a, b])
    assert len(df) == 2
    assert list(df.columns) == ["date", "message"]
