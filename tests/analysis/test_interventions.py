#  TODO: Assert number of columns equals number of users
from whatstk.analysis.interventions import get_interventions_count
from whatstk.whatsapp.objects import WhatsAppChat
from whatstk.utils.utils import COLNAMES_DF, _map_hformat_filename
import pandas as pd
import pytest

hformat = "[%d.%m.%y_%I:%M:%S_%p]_%name:"
filename = f"./tests/chats/hformats/{_map_hformat_filename(hformat)}.txt"


def test_interventions_date_all():
    chat = WhatsAppChat.from_source(filename)
    counts = get_interventions_count(chat=chat, date_mode='date', msg_length=False, all_users=True)

    assert(isinstance(counts, pd.DataFrame))
    # Asswert chat df and counts df have same users
    assert(len(counts.columns) == 1)
    assert(counts.columns == ['interventions count'])

    # Assert chat df and counts df have same date window
    assert(chat.df[COLNAMES_DF.DATE].max().date() == counts.index.max().date())
    assert(chat.df[COLNAMES_DF.DATE].min().date() == counts.index.min().date())
    

def test_interventions_date():
    chat = WhatsAppChat.from_source(filename)
    counts = get_interventions_count(chat=chat, date_mode='date', msg_length=False)

    assert(isinstance(counts, pd.DataFrame))
    # Asswert chat df and counts df have same users
    assert(set(chat.users) == set(counts.columns))
    assert(len(chat.users) == counts.shape[1])

    # Assert chat df and counts df have same date window
    assert(chat.df[COLNAMES_DF.DATE].max().date() == counts.index.max().date())
    assert(chat.df[COLNAMES_DF.DATE].min().date() == counts.index.min().date())


def test_interventions_date_2():
    chat = WhatsAppChat.from_source(filename)
    counts = get_interventions_count(df=chat.df, date_mode='date', msg_length=False)

    assert(isinstance(counts, pd.DataFrame))
    # Asswert chat df and counts df have same users
    assert(set(chat.users) == set(counts.columns))
    assert(len(chat.users) == counts.shape[1])

    # Assert chat df and counts df have same date window
    assert(chat.df[COLNAMES_DF.DATE].max().date() == counts.index.max().date())
    assert(chat.df[COLNAMES_DF.DATE].min().date() == counts.index.min().date())


def test_interventions_date_msg_length():
    chat = WhatsAppChat.from_source(filename)
    counts = get_interventions_count(chat=chat, date_mode='date', msg_length=True)

    assert(isinstance(counts, pd.DataFrame))
    # Asswert chat df and counts df have same users
    assert(set(chat.users) == set(counts.columns))
    assert(len(chat.users) == counts.shape[1])

    # Assert chat df and counts df have same date window
    assert(chat.df[COLNAMES_DF.DATE].max().date() == counts.index.max().date())
    assert(chat.df[COLNAMES_DF.DATE].min().date() == counts.index.min().date())


def test_interventions_hour():
    chat = WhatsAppChat.from_source(filename)
    counts = get_interventions_count(chat=chat, date_mode='hour', msg_length=False)

    assert(isinstance(counts, pd.DataFrame))
    # Asswert chat df and counts df have same users
    assert(set(chat.users) == set(counts.columns))
    assert(len(chat.users) == counts.shape[1])

    # Check range hours
    assert(counts.index.max() == chat.df[COLNAMES_DF.DATE].dt.hour.max())
    assert(counts.index.min() == chat.df[COLNAMES_DF.DATE].dt.hour.min())


def test_interventions_hour_msg_length():
    chat = WhatsAppChat.from_source(filename)
    counts = get_interventions_count(chat=chat, date_mode='hour', msg_length=True)

    assert(isinstance(counts, pd.DataFrame))
    # Asswert chat df and counts df have same users
    assert(set(chat.users) == set(counts.columns))
    assert(len(chat.users) == counts.shape[1])

    # Check range hours
    assert(counts.index.max() == chat.df[COLNAMES_DF.DATE].dt.hour.max())
    assert(counts.index.min() == chat.df[COLNAMES_DF.DATE].dt.hour.min())


def test_interventions_month():
    chat = WhatsAppChat.from_source(filename)
    counts = get_interventions_count(chat=chat, date_mode='month', msg_length=False)

    assert(isinstance(counts, pd.DataFrame))
    # Asswert chat df and counts df have same users
    assert(set(chat.users) == set(counts.columns))
    assert(len(chat.users) == counts.shape[1])

    # Check range months
    assert(counts.index.max() == chat.df[COLNAMES_DF.DATE].dt.month.max())
    assert(counts.index.min() == chat.df[COLNAMES_DF.DATE].dt.month.min())


def test_interventions_month_msg_length():
    chat = WhatsAppChat.from_source(filename)
    counts = get_interventions_count(chat=chat, date_mode='month', msg_length=False)

    assert(isinstance(counts, pd.DataFrame))
    # Asswert chat df and counts df have same users
    assert(set(chat.users) == set(counts.columns))
    assert(len(chat.users) == counts.shape[1])

    # Check range months
    assert(counts.index.max() == chat.df[COLNAMES_DF.DATE].dt.month.max())
    assert(counts.index.min() == chat.df[COLNAMES_DF.DATE].dt.month.min())


def test_interventions_weekday():
    chat = WhatsAppChat.from_source(filename)
    counts = get_interventions_count(chat=chat, date_mode='weekday', msg_length=False)

    assert(isinstance(counts, pd.DataFrame))
    # Asswert chat df and counts df have same users
    assert(set(chat.users) == set(counts.columns))
    assert(len(chat.users) == counts.shape[1])

    # Check range weekdays
    assert(counts.index.max() == chat.df[COLNAMES_DF.DATE].dt.weekday.max())
    assert(counts.index.min() == chat.df[COLNAMES_DF.DATE].dt.weekday.min())


def test_interventions_weekday_msg_length():
    chat = WhatsAppChat.from_source(filename)
    counts = get_interventions_count(chat=chat, date_mode='weekday', msg_length=True)

    assert(isinstance(counts, pd.DataFrame))
    # Asswert chat df and counts df have same users
    assert(set(chat.users) == set(counts.columns))
    assert(len(chat.users) == counts.shape[1])

    # Check range weekdays
    assert(counts.index.max() == chat.df[COLNAMES_DF.DATE].dt.weekday.max())
    assert(counts.index.min() == chat.df[COLNAMES_DF.DATE].dt.weekday.min())


def test_interventions_hourweekday():
    chat = WhatsAppChat.from_source(filename)
    counts = get_interventions_count(chat=chat, date_mode='hourweekday', msg_length=False)

    assert(isinstance(counts, pd.DataFrame))
    # Asswert chat df and counts df have same users
    assert(set(chat.users) == set(counts.columns))
    assert(len(chat.users) == counts.shape[1])

    # Check range weekdays
    assert(counts.index.levels[0].max() == chat.df[COLNAMES_DF.DATE].dt.weekday.max())
    assert(counts.index.levels[0].min() == chat.df[COLNAMES_DF.DATE].dt.weekday.min())

    # Check range hours
    assert(counts.index.levels[1].max() == chat.df[COLNAMES_DF.DATE].dt.hour.max())
    assert(counts.index.levels[1].min() == chat.df[COLNAMES_DF.DATE].dt.hour.min())


def test_interventions_hourweekday_msg_length():
    chat = WhatsAppChat.from_source(filename)
    counts = get_interventions_count(chat=chat, date_mode='hourweekday', msg_length=True)

    assert(isinstance(counts, pd.DataFrame))
    # Assert chat df and counts df have same users
    assert(set(chat.users) == set(counts.columns))
    assert(len(chat.users) == counts.shape[1])

    # Check range weekdays
    assert(counts.index.levels[0].max() == chat.df[COLNAMES_DF.DATE].dt.weekday.max())
    assert(counts.index.levels[0].min() == chat.df[COLNAMES_DF.DATE].dt.weekday.min())

    # Check range hours
    assert(counts.index.levels[1].max() == chat.df[COLNAMES_DF.DATE].dt.hour.max())
    assert(counts.index.levels[1].min() == chat.df[COLNAMES_DF.DATE].dt.hour.min())


def test_interventions_error_1():
    chat = WhatsAppChat.from_source(filename)
    with pytest.raises(ValueError):
        _ = get_interventions_count(chat=chat, date_mode='error', msg_length=False)
    with pytest.raises(ValueError):
        _ = get_interventions_count(chat=chat, date_mode='error', msg_length=True)


def test_interventions_error_2():
    with pytest.raises(ValueError):
        _ = get_interventions_count(date_mode='hour', msg_length=False)


def test_interventions_date_cumsum():
    chat = WhatsAppChat.from_source(filename)
    counts = get_interventions_count(chat=chat, date_mode='date', msg_length=False, cumulative=True)

    assert(isinstance(counts, pd.DataFrame))
    # Asswert chat df and counts df have same users
    assert(set(chat.users) == set(counts.columns))
    assert(len(chat.users) == counts.shape[1])

    # Assert chat df and counts df have same date window
    assert(chat.df[COLNAMES_DF.DATE].max().date() == counts.index.max().date())
    assert(chat.df[COLNAMES_DF.DATE].min().date() == counts.index.min().date())

    assert(isinstance(counts, pd.DataFrame))
    # Asswert chat df and counts df have same users
    assert(set(chat.users) == set(counts.columns))
    assert(len(chat.users) == counts.shape[1])

    # Assert chat df and counts df have same date window
    assert(chat.df[COLNAMES_DF.DATE].max().date() == counts.index.max().date())
    assert(chat.df[COLNAMES_DF.DATE].min().date() == counts.index.min().date())
