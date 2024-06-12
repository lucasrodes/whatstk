from datetime import datetime
import pandas as pd
import pytest

from whatstk.whatsapp.objects import WhatsAppChat
from whatstk._chat import BaseChat
from whatstk.utils.utils import _map_hformat_filename
from whatstk.utils.utils import COLNAMES_DF

hformat = "[%d.%m.%y_%I:%M:%S_%p]_%name:"
filepath = f"./tests/chats/hformats/{_map_hformat_filename(hformat)}.txt"


def test_properties():
    chat = WhatsAppChat.from_source(filepath)

    assert(isinstance(chat.start_date, datetime))
    assert(isinstance(chat.end_date, datetime))

def test_from_source():
    with pytest.raises(NotImplementedError):
        _ = BaseChat.from_source(filepath=filepath)


def test_from_source_2():
    chat = WhatsAppChat.from_source(filepath)
    df = chat.df

    # Fake system column
    data = {
        COLNAMES_DF.DATE: ["2020-11-21 03:02:06"],
        COLNAMES_DF.USERNAME: ["chat_name"],
        COLNAMES_DF.MESSAGE: ["chat was created"],
        COLNAMES_DF.MESSAGE_TYPE: ["system"]
    }
    df_system = pd.DataFrame(data)
    df[COLNAMES_DF.MESSAGE_TYPE] = "user"
    # Add fake row to main df
    df = pd.concat([df_system, df])
    # Ensure type of datetime
    df[COLNAMES_DF.DATE] = pd.to_datetime(df[COLNAMES_DF.DATE])
    
    chat = WhatsAppChat(df)
    assert isinstance(chat.start_date, datetime)
    assert isinstance(chat.end_date, datetime)
    assert isinstance(chat.df, pd.DataFrame)
    assert isinstance(chat.df_system, pd.DataFrame)
    assert chat.is_group
