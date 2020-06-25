import numpy as np
import pandas as pd
from datetime import datetime
from whatstk.whatsapp.objects import WhatsAppChat
from whatstk.whatsapp.generation import ChatGenerator, generate_chats_hformats


USERS = ['laurent', 'anna', 'lua', 'miquel']


def test_generate_messages():
    cg = ChatGenerator(size=10, users=USERS)
    messages = cg._generate_messages()
    assert(isinstance(messages, (list, np.ndarray)))
    assert(all([isinstance(m, str) for m in messages]))


def test_generate_emojis():
    cg = ChatGenerator(size=10, users=USERS)
    emojis = cg._generate_emojis()
    assert(isinstance(emojis, (list, np.ndarray)))
    assert(all([isinstance(e, str) for e in emojis]))


def test_generate_timestamps_1():
    cg = ChatGenerator(size=10, users=USERS)
    timestamps = cg._generate_timestamps()
    assert(isinstance(timestamps, (list, np.ndarray)))
    assert(all([isinstance(ts, datetime) for ts in timestamps]))


def test_generate_timestamps_2():
    cg = ChatGenerator(size=10, users=USERS)
    timestamps = cg._generate_timestamps(last=datetime.now())
    assert(isinstance(timestamps, (list, np.ndarray)))
    assert(all([isinstance(ts, datetime) for ts in timestamps]))


def test_generate_users():
    cg = ChatGenerator(size=10, users=USERS)
    users = cg._generate_users()
    assert(isinstance(users, (list, np.ndarray)))
    assert(all([isinstance(u, str) for u in users]))


def test_generate_df():
    cg = ChatGenerator(size=10, users=USERS)
    df = cg._generate_df()
    assert(isinstance(df, pd.DataFrame))


def test_generate_1():
    cg = ChatGenerator(size=10, users=USERS)
    chat = cg.generate()
    assert(isinstance(chat, WhatsAppChat))


def test_generate_2():
    cg = ChatGenerator(size=10, users=USERS)
    chat = cg.generate(hformat='y-%m-%d, %H:%M - %name:')
    assert(isinstance(chat, WhatsAppChat))


def test_generate_3(tmpdir):
    cg = ChatGenerator(size=10, users=USERS)
    filepath = tmpdir.join("export.txt")
    chat = cg.generate(filepath=str(filepath))
    assert(isinstance(chat, WhatsAppChat))


def test_generate_chats_hformats(tmpdir):
    output_path = tmpdir.mkdir("output")
    generate_chats_hformats(output_path, size=2, verbose=False)


def test_generate_chats_hformats_2(tmpdir):
    output_path = tmpdir.mkdir("output")
    hformat = '%Y-%m-%d, %H:%M - %name:'
    generate_chats_hformats(output_path, size=2, hformats=[hformat], filepaths=['file.txt'], verbose=False)