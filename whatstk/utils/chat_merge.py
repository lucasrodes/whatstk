"""Merging chats."""

from typing import List

import pandas as pd
from whatstk.utils.utils import COLNAMES_DF


# Temporary column used to tell apart a message genuinely sent twice from the same message
# appearing in two exports. Never present in a returned chat.
_OCCURRENCE = "_occurrence"


def _merge_key(dfs: List[pd.DataFrame]) -> List[str]:
    """Columns that identify a message, restricted to those every chat actually has.

    System-message frames carry no username, so the key is computed rather than hardcoded.

    Args:
        dfs (List[pandas.DataFrame]): Chats about to be merged.

    Returns:
        list: Column names identifying a message.
    """
    candidates = [COLNAMES_DF.DATE, COLNAMES_DF.USERNAME, COLNAMES_DF.MESSAGE]
    return [c for c in candidates if all(c in df.columns for df in dfs)]


def merge_chats(dfs: List[pd.DataFrame]) -> pd.DataFrame:
    """Merge several chats into a single one.

    Can come in handy when you have old exports and new ones, and both have relevant data.

    The result is the union of every message across the given chats, ordered by date. A message
    present in more than one chat is kept once; a message a user genuinely sent twice is kept twice.
    Two messages count as the same when their date, username and text are all equal.

    Args:
        dfs (List[pandas.DataFrame]): List with the chats as DataFrames.

    Returns:
        pandas.DataFrame: Merged chat, with a fresh RangeIndex.

    """
    key = _merge_key(dfs)
    # Numbering repeats within each chat before concatenating keeps a genuine double-send, while
    # still collapsing the copy of it that a second export of the same conversation contains.
    numbered = [df.assign(**{_OCCURRENCE: df.groupby(key, dropna=False).cumcount()}) for df in dfs]

    df = pd.concat(numbered, ignore_index=True)
    df = df.drop_duplicates(subset=key + [_OCCURRENCE], keep="first")
    df = df.drop(columns=_OCCURRENCE)
    return df.sort_values(COLNAMES_DF.DATE, kind="stable").reset_index(drop=True)
