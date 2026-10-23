import itertools

from tests.paths import TEST_CHATS_MERGE_DIR
import pandas as pd
import pytest
from whatstk.utils.chat_merge import _merge_two_chats, merge_chats
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
    df = _merge_two_chats(df1, df2)
    assert isinstance(df, pd.DataFrame)
    df = _merge_two_chats(df2, df1)
    assert isinstance(df, pd.DataFrame)


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
