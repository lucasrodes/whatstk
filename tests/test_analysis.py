from whatstk.analysis import interventions
from whatstk.objects import WhatsAppChat
import pandas as pd
import pytest
import os


filenames_path = "./tests/chats"
filenames = [os.path.join(filenames_path, f) for f in os.listdir(filenames_path) if f.endswith(".txt")]


def test_interventions_date():
    
    for filename in filenames:
        chat = WhatsAppChat.from_txt(filename)
        counts = interventions(chat, date_mode='date', msg_length=False)

        assert(isinstance(counts, pd.DataFrame))
        # Asswert chat df and counts df have same users
        assert(set(chat.users) == set(counts.columns))

        # Assert chat df and counts df have same date window
        assert(chat.df.index.max().date() == counts.index.max().date())
        assert(chat.df.index.min().date() == counts.index.min().date())


def test_interventions_date_msg_length():
    
    for filename in filenames:
        chat = WhatsAppChat.from_txt(filename)
        counts = interventions(chat, date_mode='date', msg_length=True)

        assert(isinstance(counts, pd.DataFrame))
        # Asswert chat df and counts df have same users
        assert(set(chat.users) == set(counts.columns))

        # Assert chat df and counts df have same date window
        assert(chat.df.index.max().date() == counts.index.max().date())
        assert(chat.df.index.min().date() == counts.index.min().date())


def test_interventions_hour():
    
    for filename in filenames:
        chat = WhatsAppChat.from_txt(filename)
        counts = interventions(chat, date_mode='hour', msg_length=False)

        assert(isinstance(counts, pd.DataFrame))
        # Asswert chat df and counts df have same users
        assert(set(chat.users) == set(counts.columns))

        # Check range hours
        assert(counts.index.max() == chat.df.index.hour.max())
        assert(counts.index.min() == chat.df.index.hour.min())



def test_interventions_hour_msg_length():
    
    for filename in filenames:
        chat = WhatsAppChat.from_txt(filename)
        counts = interventions(chat, date_mode='hour', msg_length=True)

        assert(isinstance(counts, pd.DataFrame))
        # Asswert chat df and counts df have same users
        assert(set(chat.users) == set(counts.columns))

        # Check range hours
        assert(counts.index.max() == chat.df.index.hour.max())
        assert(counts.index.min() == chat.df.index.hour.min())


def test_interventions_month():
    
    for filename in filenames:
        chat = WhatsAppChat.from_txt(filename)
        counts = interventions(chat, date_mode='month', msg_length=False)

        assert(isinstance(counts, pd.DataFrame))
        # Asswert chat df and counts df have same users
        assert(set(chat.users) == set(counts.columns))

        # Check range hours
        assert(counts.index.max() == chat.df.index.month.max())
        assert(counts.index.min() == chat.df.index.month.min())



def test_interventions_month_msg_length():
    
    for filename in filenames:
        chat = WhatsAppChat.from_txt(filename)
        counts = interventions(chat, date_mode='month', msg_length=False)

        assert(isinstance(counts, pd.DataFrame))
        # Asswert chat df and counts df have same users
        assert(set(chat.users) == set(counts.columns))

        # Check range hours
        assert(counts.index.max() == chat.df.index.month.max())
        assert(counts.index.min() == chat.df.index.month.min())


def test_interventions_weekday():
    
    for filename in filenames:
        chat = WhatsAppChat.from_txt(filename)
        counts = interventions(chat, date_mode='weekday', msg_length=False)

        assert(isinstance(counts, pd.DataFrame))
        # Asswert chat df and counts df have same users
        assert(set(chat.users) == set(counts.columns))

        # Check range hours
        assert(counts.index.max() == chat.df.index.weekday.max())
        assert(counts.index.min() == chat.df.index.weekday.min())



def test_interventions_weekday_msg_length():
    
    for filename in filenames:
        chat = WhatsAppChat.from_txt(filename)
        counts = interventions(chat, date_mode='weekday', msg_length=True)

        assert(isinstance(counts, pd.DataFrame))
        # Asswert chat df and counts df have same users
        assert(set(chat.users) == set(counts.columns))

        # Check range hours
        assert(counts.index.max() == chat.df.index.weekday.max())
        assert(counts.index.min() == chat.df.index.weekday.min())



def test_interventions_hourweekday():
    
    for filename in filenames:
        chat = WhatsAppChat.from_txt(filename)
        counts = interventions(chat, date_mode='hourweekday', msg_length=False)

        assert(isinstance(counts, pd.DataFrame))
        # Asswert chat df and counts df have same users
        assert(set(chat.users) == set(counts.columns))

        # Check range days
        assert(counts.index.levels[0].max() == chat.df.index.weekday.max())
        assert(counts.index.levels[0].min() == chat.df.index.weekday.min())

        # Check range hours
        assert(counts.index.levels[1].max() == chat.df.index.hour.max())
        assert(counts.index.levels[1].min() == chat.df.index.hour.min())


def test_interventions_hourweekday_msg_length():
    
    for filename in filenames:
        chat = WhatsAppChat.from_txt(filename)
        counts = interventions(chat, date_mode='hourweekday', msg_length=True)

        assert(isinstance(counts, pd.DataFrame))
        # Asswert chat df and counts df have same users
        assert(set(chat.users) == set(counts.columns))

        # Check range days
        assert(counts.index.levels[0].max() == chat.df.index.weekday.max())
        assert(counts.index.levels[0].min() == chat.df.index.weekday.min())

        # Check range hours
        assert(counts.index.levels[1].max() == chat.df.index.hour.max())
        assert(counts.index.levels[1].min() == chat.df.index.hour.min())

def test_interventions_error():
    
    for filename in filenames:
        chat = WhatsAppChat.from_txt(filename)
        with pytest.raises(ValueError):
            counts = interventions(chat, date_mode='error', msg_length=False)
        with pytest.raises(ValueError):
            counts = interventions(chat, date_mode='error', msg_length=True)
