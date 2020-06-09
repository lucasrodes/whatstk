from datetime import datetime
from whatstk.whatsapp.objects import WhatsAppChat


filename = "./tests/chats/hformats/[%d.%m.%y_%I:%M:%S_%p]_%name:.txt"


def test_properties():
    chat = WhatsAppChat.from_txt(filename)

    assert(isinstance(chat.start_date, datetime))
    assert(isinstance(chat.end_date, datetime))
