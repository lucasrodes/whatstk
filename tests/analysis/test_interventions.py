#  TODO: Assert number of columns equals number of users
from whatstk.analysis.interventions import get_interventions_count
from whatstk.whatsapp.objects import WhatsAppChat
import pandas as pd
import pytest


filename = "./tests/chats/hformats/[%d.%m.%y_%I:%M:%S_%p]_%name:.txt"


def test_interventions_date():
    chat = WhatsAppChat.from_txt(filename)
    counts = get_interventions_count(chat=chat, date_mode='date', msg_length=False)

    assert(isinstance(counts, pd.DataFrame))
    # Asswert chat df and counts df have same users
    assert(set(chat.users) == set(counts.columns))
    assert(len(chat.users) == counts.shape[1])

    # Assert chat df and counts df have same date window
    assert(chat.df.index.max().date() == counts.index.max().date())
    assert(chat.df.index.min().date() == counts.index.min().date())


def test_interventions_date_2():
    chat = WhatsAppChat.from_txt(filename)
    counts = get_interventions_count(df=chat.df, date_mode='date', msg_length=False)

    assert(isinstance(counts, pd.DataFrame))
    # Asswert chat df and counts df have same users
    assert(set(chat.users) == set(counts.columns))
    assert(len(chat.users) == counts.shape[1])

    # Assert chat df and counts df have same date window
    assert(chat.df.index.max().date() == counts.index.max().date())
    assert(chat.df.index.min().date() == counts.index.min().date())


def test_interventions_date_msg_length():
    chat = WhatsAppChat.from_txt(filename)
    counts = get_interventions_count(chat=chat, date_mode='date', msg_length=True)

    assert(isinstance(counts, pd.DataFrame))
    # Asswert chat df and counts df have same users
    assert(set(chat.users) == set(counts.columns))
    assert(len(chat.users) == counts.shape[1])

    # Assert chat df and counts df have same date window
    assert(chat.df.index.max().date() == counts.index.max().date())
    assert(chat.df.index.min().date() == counts.index.min().date())


def test_interventions_hour():
    chat = WhatsAppChat.from_txt(filename)
    counts = get_interventions_count(chat=chat, date_mode='hour', msg_length=False)

    assert(isinstance(counts, pd.DataFrame))
    # Asswert chat df and counts df have same users
    assert(set(chat.users) == set(counts.columns))
    assert(len(chat.users) == counts.shape[1])

    # Check range hours
    assert(counts.index.max() == chat.df.index.hour.max())
    assert(counts.index.min() == chat.df.index.hour.min())


def test_interventions_hour_msg_length():
    chat = WhatsAppChat.from_txt(filename)
    counts = get_interventions_count(chat=chat, date_mode='hour', msg_length=True)

    assert(isinstance(counts, pd.DataFrame))
    # Asswert chat df and counts df have same users
    assert(set(chat.users) == set(counts.columns))
    assert(len(chat.users) == counts.shape[1])

    # Check range hours
    assert(counts.index.max() == chat.df.index.hour.max())
    assert(counts.index.min() == chat.df.index.hour.min())


def test_interventions_month():
    chat = WhatsAppChat.from_txt(filename)
    counts = get_interventions_count(chat=chat, date_mode='month', msg_length=False)

    assert(isinstance(counts, pd.DataFrame))
    # Asswert chat df and counts df have same users
    assert(set(chat.users) == set(counts.columns))
    assert(len(chat.users) == counts.shape[1])

    # Check range hours
    assert(counts.index.max() == chat.df.index.month.max())
    assert(counts.index.min() == chat.df.index.month.min())


def test_interventions_month_msg_length():
    chat = WhatsAppChat.from_txt(filename)
    counts = get_interventions_count(chat=chat, date_mode='month', msg_length=False)

    assert(isinstance(counts, pd.DataFrame))
    # Asswert chat df and counts df have same users
    assert(set(chat.users) == set(counts.columns))
    assert(len(chat.users) == counts.shape[1])

    # Check range hours
    assert(counts.index.max() == chat.df.index.month.max())
    assert(counts.index.min() == chat.df.index.month.min())


def test_interventions_weekday():
    chat = WhatsAppChat.from_txt(filename)
    counts = get_interventions_count(chat=chat, date_mode='weekday', msg_length=False)

    assert(isinstance(counts, pd.DataFrame))
    # Asswert chat df and counts df have same users
    assert(set(chat.users) == set(counts.columns))
    assert(len(chat.users) == counts.shape[1])

    # Check range hours
    assert(counts.index.max() == chat.df.index.weekday.max())
    assert(counts.index.min() == chat.df.index.weekday.min())


def test_interventions_weekday_msg_length():
    chat = WhatsAppChat.from_txt(filename)
    counts = get_interventions_count(chat=chat, date_mode='weekday', msg_length=True)

    assert(isinstance(counts, pd.DataFrame))
    # Asswert chat df and counts df have same users
    assert(set(chat.users) == set(counts.columns))
    assert(len(chat.users) == counts.shape[1])

    # Check range hours
    assert(counts.index.max() == chat.df.index.weekday.max())
    assert(counts.index.min() == chat.df.index.weekday.min())


def test_interventions_hourweekday():
    chat = WhatsAppChat.from_txt(filename)
    counts = get_interventions_count(chat=chat, date_mode='hourweekday', msg_length=False)

    assert(isinstance(counts, pd.DataFrame))
    # Asswert chat df and counts df have same users
    assert(set(chat.users) == set(counts.columns))
    assert(len(chat.users) == counts.shape[1])

    # Check range days
    assert(counts.index.levels[0].max() == chat.df.index.weekday.max())
    assert(counts.index.levels[0].min() == chat.df.index.weekday.min())

    # Check range hours
    assert(counts.index.levels[1].max() == chat.df.index.hour.max())
    assert(counts.index.levels[1].min() == chat.df.index.hour.min())


def test_interventions_hourweekday_msg_length():
    chat = WhatsAppChat.from_txt(filename)
    counts = get_interventions_count(chat=chat, date_mode='hourweekday', msg_length=True)

    assert(isinstance(counts, pd.DataFrame))
    # Assert chat df and counts df have same users
    assert(set(chat.users) == set(counts.columns))
    assert(len(chat.users) == counts.shape[1])

    # Check range days
    assert(counts.index.levels[0].max() == chat.df.index.weekday.max())
    assert(counts.index.levels[0].min() == chat.df.index.weekday.min())

    # Check range hours
    assert(counts.index.levels[1].max() == chat.df.index.hour.max())
    assert(counts.index.levels[1].min() == chat.df.index.hour.min())


def test_interventions_error_1():
    chat = WhatsAppChat.from_txt(filename)
    with pytest.raises(ValueError):
        _ = get_interventions_count(chat=chat, date_mode='error', msg_length=False)
    with pytest.raises(ValueError):
        _ = get_interventions_count(chat=chat, date_mode='error', msg_length=True)


def test_interventions_error_2():
    with pytest.raises(ValueError):
        _ = get_interventions_count(date_mode='hour', msg_length=False)


def test_interventions_date_cumsum():
    chat = WhatsAppChat.from_txt(filename)
    counts = get_interventions_count(chat=chat, date_mode='date', msg_length=False, cummulative=True)

    assert(isinstance(counts, pd.DataFrame))
    # Asswert chat df and counts df have same users
    assert(set(chat.users) == set(counts.columns))
    assert(len(chat.users) == counts.shape[1])

    # Assert chat df and counts df have same date window
    assert(chat.df.index.max().date() == counts.index.max().date())
    assert(chat.df.index.min().date() == counts.index.min().date())
