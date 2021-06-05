import os

import pandas as pd
import pytest

from whatstk.whatsapp.objects import WhatsAppChat
from whatstk.utils.exceptions import HFormatError
from whatstk.utils.utils import _map_hformat_filename


hformat = "[%d.%m.%y %I:%M:%S %p] %name:"
filename = f"./tests/chats/hformats/{_map_hformat_filename(hformat)}.txt"

chats_merge_path = 'tests/chats/merge/'
filename1 = os.path.join(chats_merge_path, 'file1.txt')
filename2 = os.path.join(chats_merge_path, 'file2.txt')
hformat_merge = '%y-%m-%d, %H:%M - %name:'


def test_object_auto():
    chat = WhatsAppChat.from_source(filename)
    assert(isinstance(chat.df, pd.DataFrame))


def test_object_hformat():
    chat = WhatsAppChat.from_source(filename)
    assert(isinstance(chat.df, pd.DataFrame))

    chat = WhatsAppChat.from_source(filename)
    assert(isinstance(chat.df, pd.DataFrame))


def test_object_error():
    with pytest.raises(ValueError):
        _ = WhatsAppChat.from_source(filename, auto_header=False)


def test_object_to_csv_1(tmpdir):
    chat = WhatsAppChat.from_source(filename)
    filename_ = tmpdir.join("export.csv")
    chat.to_csv(filepath=str(filename_))


def test_object_to_csv_2(tmpdir):
    chat = WhatsAppChat.from_source(filename)
    filename_ = tmpdir.join("export")
    with pytest.raises(ValueError):
        chat.to_csv(filepath=str(filename_))


def test_object_to_txt(tmpdir):
    chat = WhatsAppChat.from_source(filename)
    filename_ = tmpdir.join("export")
    with pytest.raises(ValueError):
        chat.to_txt(filepath=str(filename_))


def test_object_from_source_error(tmpdir):
    with pytest.raises((HFormatError, KeyError)):
        _ = WhatsAppChat.from_source(filename, hformat="%y%name")


def test_object_from_sources(tmpdir):
    chat = WhatsAppChat.from_sources([filename1, filename2])
    assert(isinstance(chat.df, pd.DataFrame))
    chat = WhatsAppChat.from_sources([filename2, filename1])
    assert(isinstance(chat.df, pd.DataFrame))
    chat = WhatsAppChat.from_sources([filename2, filename1], auto_header=True)
    assert(isinstance(chat.df, pd.DataFrame))
    hformat = [hformat_merge, hformat_merge]
    chat = WhatsAppChat.from_sources([filename2, filename1], auto_header=False, hformat=hformat)
    assert(isinstance(chat.df, pd.DataFrame))


def test_merge():
    chat1 = WhatsAppChat.from_source(filename1)
    chat2 = WhatsAppChat.from_source(filename2)
    chat = chat1.merge(chat2)
    assert(isinstance(chat.df, pd.DataFrame))
    chat = chat1.merge(chat2, rename_users={'J': ['John']})
    assert(isinstance(chat.df, pd.DataFrame))


def test_rename_users():
    chat = WhatsAppChat.from_source(filename)
    chat = chat.rename_users(mapping={'J': ['John']})
    assert(isinstance(chat.df, pd.DataFrame))


def test_rename_users_error():
    chat = WhatsAppChat.from_source(filename)
    with pytest.raises(ValueError):
        chat = chat.rename_users(mapping={'J': 'John'})


def test_len():
    chat = WhatsAppChat.from_source(filename)
    assert(isinstance(len(chat), int))
