import pytest
import plotly.graph_objs as go

from whatstk.graph.base import FigureBuilder
from whatstk.whatsapp.objects import WhatsAppChat
from whatstk.utils.utils import _map_hformat_filename


hformat = "[%d.%m.%y_%I:%M:%S_%p]_%name:"
filename = f"./tests/chats/hformats/{_map_hformat_filename(hformat)}.txt"


def load_chat_as_df():
    return WhatsAppChat.from_source(filename).df


def load_chat():
    return WhatsAppChat.from_source(filename)


def test_init():
    df = load_chat_as_df()
    _ = FigureBuilder(df=df)
    chat = load_chat()
    _ = FigureBuilder(chat=chat)
    with pytest.raises(ValueError):
        _ = FigureBuilder()


def test_init_mapping_dict_1():
    df = load_chat_as_df()
    fb = FigureBuilder(df=df)
    mapping = fb.user_color_mapping
    assert(isinstance(fb.user_color_mapping, dict))
    assert(len(mapping) == df['username'].nunique())


def test_init_mapping_dict_2():
    df = load_chat_as_df()
    fb = FigureBuilder(df=df)
    value = {'a': 'b'}
    fb.user_color_mapping = value
    assert(fb.user_color_mapping == value)


def test_user_msg_length_boxplot():
    df = load_chat_as_df()
    fb = FigureBuilder(df=df)
    fig = fb.user_msg_length_boxplot()
    assert isinstance(fig, go.Figure)
    assert ('data' in fig and 'layout' in fig)


def test_user_interventions_count_linechart():
    df = load_chat_as_df()
    fb = FigureBuilder(df=df)
    fig = fb.user_interventions_count_linechart()
    assert isinstance(fig, go.Figure)
    assert ('data' in fig and 'layout' in fig)

def test_user_interventions_count_linechart_2():
    df = load_chat_as_df()
    fb = FigureBuilder(df=df)
    fig = fb.user_interventions_count_linechart(all_users=True)
    assert isinstance(fig, go.Figure)
    assert ('data' in fig and 'layout' in fig)


def test_user_message_responses_flow():
    df = load_chat_as_df()
    fb = FigureBuilder(df=df)
    fig = fb.user_message_responses_flow()
    assert isinstance(fig, go.Figure)
    assert ('data' in fig and 'layout' in fig)


def test_user_message_responses_heatmap():
    df = load_chat_as_df()
    fb = FigureBuilder(df=df)
    fig = fb.user_message_responses_heatmap()
    assert isinstance(fig, go.Figure)
    assert ('data' in fig and 'layout' in fig)
