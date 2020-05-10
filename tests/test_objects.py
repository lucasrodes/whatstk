from whatstk.objects import WhatsAppChat
from whatstk.utils.exceptions import HFormatError
import os
import pandas as pd
import pytest


filename = "./tests/chats/[%d.%m.%y_%I:%M:%S_%p]_%name:.txt"
hformat = "[%d.%m.%y %I:%M:%S %p] %name:"


def test_object_auto():
    chat = WhatsAppChat.from_txt(filename)
    assert(isinstance(chat.df, pd.DataFrame))


def test_object_hformat():
    chat = WhatsAppChat.from_txt(filename)
    assert(isinstance(chat.df, pd.DataFrame))

    chat = WhatsAppChat.from_txt(filename)
    assert(isinstance(chat.df, pd.DataFrame))


def test_object_error():
    with pytest.raises(ValueError):
        chat = WhatsAppChat.from_txt(filename, auto_header=False)


def test_object_len_shape():
    chat = WhatsAppChat.from_txt(filename)
    l = len(chat)
    assert(isinstance(l, int))
    s = chat.shape
    assert(isinstance(s, tuple))
    assert(len(s)==2)


def test_object_to_csv_1(tmpdir):
    chat = WhatsAppChat.from_txt(filename)
    filename_ = tmpdir.join("export.csv")
    chat.to_csv(filename=str(filename_))


def test_object_to_csv_2(tmpdir):
    chat = WhatsAppChat.from_txt(filename)
    filename_ = tmpdir.join("export")
    with pytest.raises(ValueError):
        chat.to_csv(filename=str(filename_))


def test_object_to_txt(tmpdir):
    chat = WhatsAppChat.from_txt(filename)
    filename_ = tmpdir.join("export")
    with pytest.raises(ValueError):
        chat.to_txt(filename=str(filename_))


def test_object_from_txt_error(tmpdir):
    with pytest.raises((HFormatError, KeyError)):
        chat = WhatsAppChat.from_txt(filename, hformat="%y%name")