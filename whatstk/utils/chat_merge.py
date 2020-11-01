"""Merging chats."""


import pandas as pd
from whatstk.utils.utils import COLNAMES_DF


def _merge_two_chats(df1, df2):
    if df1[COLNAMES_DF.DATE].min() <= df2[COLNAMES_DF.DATE].min():
        df = pd.concat([df1, df2[df2[COLNAMES_DF.DATE] > df1[COLNAMES_DF.DATE].max()]])
    else:
        df = pd.concat([df2, df1[df1[COLNAMES_DF.DATE] > df2[COLNAMES_DF.DATE].max()]])
    return df


def merge_chats(dfs):
    """Merge several chats into a single one.

    Can come in handy when you have old exports and new ones, and both have relevant data.

    **Note:** The dataframes must have an index with the timestamps of the messages, as this is required to correctly
    sort and merge the chats.

    Args:
        dfs (List[pandas.DataFrame]): List with the chats as DataFrames.

    Returns:
        pandas.DataFrame: Merged chat.

    """
    # Sort from oldest
    dfs = sorted(dfs, key=lambda x: x.index.min())
    # Merge
    df = dfs[0]
    for i in range(1, len(dfs)):
        df = _merge_two_chats(df, dfs[i])
    return df
