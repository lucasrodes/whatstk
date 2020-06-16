import pytest
from datetime import datetime
from whatstk.whatsapp.objects import WhatsAppChat


filepath = "./tests/chats/hformats/[%d.%m.%y_%I:%M:%S_%p]_%name:.txt"


def test_properties():
    chat = WhatsAppChat.from_source(filepath)

    assert(isinstance(chat.start_date, datetime))
    assert(isinstance(chat.end_date, datetime))

def test_from_source():
    chat = WhatsAppChat.from_source(filepath)
    with pytest.raises(NotImplementedError):
        _ = chat.from_source()