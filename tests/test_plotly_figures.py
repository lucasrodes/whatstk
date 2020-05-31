import pytest
from whatstk.plotly.figures.base import FigureBuilder
from whatstk.objects import WhatsAppChat


filename = "./tests/chats/hformats/[%d.%m.%y_%I:%M:%S_%p]_%name:.txt"


def load_chat_as_df():
    return WhatsAppChat.from_txt(filename).df


def load_chat():
    return WhatsAppChat.from_txt(filename)


def test_init():
    df = load_chat_as_df()
    _ = FigureBuilder(df=df)
    chat = load_chat()
    _ = FigureBuilder(chat=chat)
    with pytest.raises(ValueError):
        _ = FigureBuilder()


def test_user_msg_length_boxplot():
    df = load_chat_as_df()
    fb = FigureBuilder(df=df)
    fig = fb.user_msg_length_boxplot()
    assert isinstance(fig, dict)
    assert ('data' in fig and 'layout' in fig)


def test_user_interventions_count_linechart():
    df = load_chat_as_df()
    fb = FigureBuilder(df=df)
    fig = fb.user_interventions_count_linechart()
    assert isinstance(fig, dict)
    assert ('data' in fig and 'layout' in fig)
