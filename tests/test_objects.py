from whatstk.objects import WhatsAppChat
import pandas as pd


def test_object_auto():
    filename = 'tests/chats/example_1.txt'
    chat = WhatsAppChat.from_txt(filename)
    assert(isinstance(chat.df, pd.DataFrame))

    filename = 'tests/chats/example_2.txt'
    chat = WhatsAppChat.from_txt(filename)
    assert(isinstance(chat.df, pd.DataFrame))


def test_object_hformat():
    filename = 'tests/chats/example_1.txt'
    hformat = '%d.%m.%y, %H:%M - %name:'
    chat = WhatsAppChat.from_txt(filename)
    assert(isinstance(chat.df, pd.DataFrame))

    filename = 'tests/chats/example_2.txt'
    hformat = '[%y/%m/%d %H:%M] %name:'
    chat = WhatsAppChat.from_txt(filename)
    assert(isinstance(chat.df, pd.DataFrame))
