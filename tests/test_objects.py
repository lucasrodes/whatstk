from whatstk.objects import WhatsAppChat
import pandas as pd


def test_object_auto():
    filename = './chats/example.txt'
    chat = WhatsAppChat.from_txt(filename)
    assert(isinstance(chat.df, pd.DataFrame))


def test_object_hformat():
    filename = './chats/example.txt'
    hformat = '%d.%m.%y, %H:%M - %name:'
    chat = WhatsAppChat.from_txt(filename)
    assert(isinstance(chat.df, pd.DataFrame))


