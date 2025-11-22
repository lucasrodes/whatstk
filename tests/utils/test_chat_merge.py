from tests.paths import TEST_CHATS_MERGE_DIR
import pandas as pd
from whatstk.utils.chat_merge import _merge_two_chats
from whatstk.whatsapp.parser import df_from_whatsapp


filename1 = str(TEST_CHATS_MERGE_DIR / "file1.txt")
filename2 = str(TEST_CHATS_MERGE_DIR / "file2.txt")


def test_merge_two_chats():
    df1 = df_from_whatsapp(filename1)
    df2 = df_from_whatsapp(filename2)
    df = _merge_two_chats(df1, df2)
    assert isinstance(df, pd.DataFrame)
    df = _merge_two_chats(df2, df1)
    assert isinstance(df, pd.DataFrame)
