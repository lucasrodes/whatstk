"""Merge utils."""


import pandas as pd


def _merge_two_chats(df1, df2):
    if df1.index.min() <= df2.index.min():
        df = pd.concat([df1, df2[df2.index > df1.index.max()]])
    else:
        df = pd.concat([df2, df1[df1.index > df2.index.max()]])
    return df


def merge_chats(dfs):
    """Merge several chats into a single one.

    Can come in handy when you have old exports and new ones, and both have relevant data.

    Args:
        dfs (list): List with the chats as DataFrames.

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
