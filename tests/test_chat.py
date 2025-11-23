from datetime import datetime
from tests.paths import TEST_CHATS_HFORMATS_DIR
import pandas as pd
import pytest

from whatstk.whatsapp.objects import WhatsAppChat
from whatstk._chat import BaseChat
from whatstk.utils.utils import _map_hformat_filename
from whatstk.utils.utils import COLNAMES_DF

hformat = "[%d.%m.%y_%I:%M:%S_%p]_%name:"
filepath = f"{TEST_CHATS_HFORMATS_DIR}/{_map_hformat_filename(hformat)}.txt"


def test_properties():
    chat = WhatsAppChat.from_source(filepath)

    assert isinstance(chat.start_date, datetime)
    assert isinstance(chat.end_date, datetime)


def test_from_source():
    with pytest.raises(NotImplementedError):
        _ = BaseChat.from_source(filepath=filepath)


def test_from_source_2():
    chat = WhatsAppChat.from_source(filepath)
    df = chat.df

    # Fake system column
    data = {
        COLNAMES_DF.DATE: ["2020-11-21 03:02:06"],
        COLNAMES_DF.USERNAME: ["chat_name"],
        COLNAMES_DF.MESSAGE: ["chat was created"],
        COLNAMES_DF.MESSAGE_TYPE: ["system"],
    }
    df_system = pd.DataFrame(data)
    df[COLNAMES_DF.MESSAGE_TYPE] = "user"
    # Add fake row to main df
    df = pd.concat([df_system, df])
    # Ensure type of datetime
    df[COLNAMES_DF.DATE] = pd.to_datetime(df[COLNAMES_DF.DATE])

    chat = WhatsAppChat(df)
    assert isinstance(chat.start_date, datetime)
    assert isinstance(chat.end_date, datetime)
    assert isinstance(chat.df, pd.DataFrame)
    assert isinstance(chat.df_system, pd.DataFrame)
    assert chat.is_group


def test_is_group_false():
    """Test is_group returns False for non-group chats (2 users or less)."""
    chat = WhatsAppChat.from_source(filepath)
    df = chat.df
    # Create a chat with only 2 users (not a group)
    df_two_users = df[df[COLNAMES_DF.USERNAME].isin(df[COLNAMES_DF.USERNAME].unique()[:2])]
    chat_two_users = WhatsAppChat(df_two_users)
    assert not chat_two_users.is_group


def test_system_messages_invalid_usernames():
    """Test ValueError when system messages have multiple different usernames."""
    chat = WhatsAppChat.from_source(filepath)
    df = chat.df

    # Create system messages with DIFFERENT usernames (invalid)
    data = {
        COLNAMES_DF.DATE: ["2020-11-21 03:02:06", "2020-11-21 03:02:07"],
        COLNAMES_DF.USERNAME: ["chat_name1", "chat_name2"],  # Different names - invalid!
        COLNAMES_DF.MESSAGE: ["chat was created", "settings changed"],
        COLNAMES_DF.MESSAGE_TYPE: ["system", "system"],
    }
    df_system = pd.DataFrame(data)
    df[COLNAMES_DF.MESSAGE_TYPE] = "user"
    df = pd.concat([df_system, df])
    df[COLNAMES_DF.DATE] = pd.to_datetime(df[COLNAMES_DF.DATE])

    with pytest.raises(ValueError, match="System messages dataframe must contain only one username"):
        WhatsAppChat(df)


def test_non_group_with_message_type():
    """Test that message_type column is dropped for non-group chats."""
    chat = WhatsAppChat.from_source(filepath)
    df = chat.df

    # Create a non-group chat (2 users) with message_type column
    df_two_users = df[df[COLNAMES_DF.USERNAME].isin(df[COLNAMES_DF.USERNAME].unique()[:2])].copy()
    df_two_users[COLNAMES_DF.MESSAGE_TYPE] = "user"

    chat_two_users = WhatsAppChat(df_two_users)

    # Message type should be dropped since it's not a group
    assert COLNAMES_DF.MESSAGE_TYPE not in chat_two_users.df.columns
    assert not chat_two_users.is_group


def test_merge_platform_mismatch():
    """Test ValueError when merging chats from different platforms."""
    from tests.paths import TEST_CHATS_MERGE_DIR
    import os

    filename1 = os.path.join(TEST_CHATS_MERGE_DIR, "file1.txt")
    chat1 = WhatsAppChat.from_source(filename1)
    chat2 = WhatsAppChat.from_source(filename1)

    # Manually set different platforms
    chat1._platform = "whatsapp"
    chat2._platform = "telegram"  # Different platform

    with pytest.raises(ValueError, match="Both chats must come from the same platform"):
        chat1.merge(chat2)


def test_merge_with_df_system():
    """Test merging two chats that both have df_system."""
    from tests.paths import TEST_CHATS_MERGE_DIR
    import os

    filename1 = os.path.join(TEST_CHATS_MERGE_DIR, "file1.txt")

    # Create two chats with system messages
    chat1 = WhatsAppChat.from_source(filename1)
    df1 = chat1.df.copy()

    # Add system messages to both chats
    data_system = {
        COLNAMES_DF.DATE: ["2019-01-01 00:00:00"],
        COLNAMES_DF.USERNAME: ["Group Chat"],
        COLNAMES_DF.MESSAGE: ["Group created"],
        COLNAMES_DF.MESSAGE_TYPE: ["system"],
    }
    df_system = pd.DataFrame(data_system)
    df_system[COLNAMES_DF.DATE] = pd.to_datetime(df_system[COLNAMES_DF.DATE])
    df1[COLNAMES_DF.MESSAGE_TYPE] = "user"
    df1_full = pd.concat([df_system, df1])

    chat1_with_system = WhatsAppChat(df1_full)
    chat2_with_system = WhatsAppChat(df1_full)

    # Merge should combine both df_system
    merged = chat1_with_system.merge(chat2_with_system)

    assert len(merged.df_system) > 0
    assert isinstance(merged.df_system, pd.DataFrame)


def test_filter_dates():
    """Test filter_dates method."""
    chat = WhatsAppChat.from_source(filepath)
    
    start = chat.start_date
    end = chat.end_date
    mid = start + (end - start) / 2
    
    # Test date_min
    chat_min = chat.filter_dates(date_min=mid)
    assert chat_min.start_date >= mid
    assert len(chat_min) < len(chat)
    
    # Test date_max
    chat_max = chat.filter_dates(date_max=mid)
    assert chat_max.end_date <= mid
    assert len(chat_max) < len(chat)
    
    # Test both
    # Ensure we pick a range that includes some messages but not all
    # Let's pick q1 and q3
    q1 = start + (end - start) / 4
    q3 = start + 3 * (end - start) / 4
    
    chat_both = chat.filter_dates(date_min=q1, date_max=q3)
    assert chat_both.start_date >= q1
    assert chat_both.end_date <= q3
    assert len(chat_both) < len(chat)
    
    # Test no filter
    chat_none = chat.filter_dates()
    assert len(chat_none) == len(chat)
    pd.testing.assert_frame_equal(chat_none.df, chat.df)
    
    # Test empty result
    future_date = end + pd.Timedelta(days=365)
    chat_empty = chat.filter_dates(date_min=future_date)
    assert len(chat_empty) == 0
    assert chat_empty.df.empty
