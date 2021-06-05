from datetime import datetime

import pytest

from whatstk.whatsapp.objects import WhatsAppChat
from whatstk._chat import BaseChat
from whatstk.utils.utils import _map_hformat_filename

hformat = "[%d.%m.%y_%I:%M:%S_%p]_%name:"
filepath = f"./tests/chats/hformats/{_map_hformat_filename(hformat)}.txt"


def test_properties():
    chat = WhatsAppChat.from_source(filepath)

    assert(isinstance(chat.start_date, datetime))
    assert(isinstance(chat.end_date, datetime))

def test_from_source():
    with pytest.raises(NotImplementedError):
        _ = BaseChat.from_source(filepath=filepath)
