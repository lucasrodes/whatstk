from whatstk.objects import WhatsAppChat
import os
import pandas as pd
import pytest


filenames_path = "./tests/chats"
filenames = [os.path.join(filenames_path, f) for f in os.listdir(filenames_path) if f.endswith(".txt")]


def test_object_auto():
    for filename in filenames:
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


def test_object_error():
    for filename in filenames:
        with pytest.raises(ValueError):
            chat = WhatsAppChat.from_txt(filename, auto_header=False)


def test_object_len_shape():
    filename = 'tests/chats/example_1.txt'
    hformat = '%d.%m.%y, %H:%M - %name:'
    chat = WhatsAppChat.from_txt(filename)
    l = len(chat)
    assert(isinstance(l, int))
    s = chat.shape
    assert(isinstance(s, tuple))
    assert(len(s)==2)
