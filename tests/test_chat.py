import pytest
from datetime import datetime
from whatstk.whatsapp.objects import WhatsAppChat
from whatstk._chat import BaseChat


filepath = "./tests/chats/hformats/[%d.%m.%y_%I:%M:%S_%p]_%name:.txt"


def test_properties():
    chat = WhatsAppChat.from_source(filepath)

    assert(isinstance(chat.start_date, datetime))
    assert(isinstance(chat.end_date, datetime))

def test_from_source():
    with pytest.raises(NotImplementedError):
        _ = BaseChat.from_source(filepath=filepath)