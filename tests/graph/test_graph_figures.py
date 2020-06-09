import pytest
from whatstk.graph.base import FigureBuilder
from whatstk.whatsapp.objects import WhatsAppChat


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
    assert isinstance(fig, dict)
    assert ('data' in fig and 'layout' in fig)


def test_user_interventions_count_linechart():
    df = load_chat_as_df()
    fb = FigureBuilder(df=df)
    fig = fb.user_interventions_count_linechart()
    assert isinstance(fig, dict)
    assert ('data' in fig and 'layout' in fig)


def test_user_message_responses_flow():
    df = load_chat_as_df()
    fb = FigureBuilder(df=df)
    fig = fb.user_message_responses_flow()
    assert isinstance(fig, dict)
    assert ('data' in fig and 'layout' in fig)


def test_user_message_responses_heatmap():
    df = load_chat_as_df()
    fb = FigureBuilder(df=df)
    fig = fb.user_message_responses_heatmap()
    assert isinstance(fig, dict)
    assert ('data' in fig and 'layout' in fig)
