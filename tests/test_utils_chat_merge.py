import os
import pandas as pd
from whatstk.utils.chat_merge import _merge_two_chats
from whatstk.core import df_from_txt


chats_merge_path = 'tests/chats/merge/'
filename1 = os.path.join(chats_merge_path, 'file1.txt')
filename2 = os.path.join(chats_merge_path, 'file2.txt')



def test_merge_two_chats():
    df1 = df_from_txt(filename1)
    df2 = df_from_txt(filename2)
    df = _merge_two_chats(df1, df2)
    assert(isinstance(df, pd.DataFrame))
    df = _merge_two_chats(df2, df1)
    assert(isinstance(df, pd.DataFrame))