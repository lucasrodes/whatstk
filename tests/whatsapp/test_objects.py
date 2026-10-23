from tests.paths import TEST_CHATS_HFORMATS_DIR, TEST_CHATS_MERGE_DIR, CHATS_DIR

import pandas as pd
import pytest

from whatstk.whatsapp.objects import WhatsAppChat
from whatstk.utils.exceptions import HFormatError
from whatstk.utils.utils import _map_hformat_filename


hformat = "[%d.%m.%y %I:%M:%S %p] %name:"
filename = str(TEST_CHATS_HFORMATS_DIR / "{}.txt".format(_map_hformat_filename(hformat)))

filename1 = str(TEST_CHATS_MERGE_DIR / "file1.txt")
filename2 = str(TEST_CHATS_MERGE_DIR / "file2.txt")
hformat_merge = "%y-%m-%d, %H:%M - %name:"


def test_object_auto():
    chat = WhatsAppChat.from_source(filename)
    assert isinstance(chat.df, pd.DataFrame)


def test_object_hformat():
    chat = WhatsAppChat.from_source(filename)
    assert isinstance(chat.df, pd.DataFrame)

    chat = WhatsAppChat.from_source(filename)
    assert isinstance(chat.df, pd.DataFrame)


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


def test_object_to_zip(tmpdir):
    chat = WhatsAppChat.from_source(filename)
    filename_ = tmpdir.join("export")
    print(filename_)
    with pytest.raises(ValueError):
        chat.to_zip(filepath=str(filename_))


def test_object_from_source_error(tmpdir):
    with pytest.raises((HFormatError, KeyError)):
        _ = WhatsAppChat.from_source(filename, hformat="%y%name")


def test_object_from_sources(tmpdir):
    chat = WhatsAppChat.from_sources([filename1, filename2])
    assert isinstance(chat.df, pd.DataFrame)
    chat = WhatsAppChat.from_sources([filename2, filename1])
    assert isinstance(chat.df, pd.DataFrame)
    chat = WhatsAppChat.from_sources([filename2, filename1], auto_header=True)
    assert isinstance(chat.df, pd.DataFrame)
    hformat = [hformat_merge, hformat_merge]
    chat = WhatsAppChat.from_sources([filename2, filename1], auto_header=False, hformat=hformat)
    assert isinstance(chat.df, pd.DataFrame)


def test_merge():
    chat1 = WhatsAppChat.from_source(filename1)
    chat2 = WhatsAppChat.from_source(filename2)
    chat = chat1.merge(chat2)
    assert isinstance(chat.df, pd.DataFrame)
    chat = chat1.merge(chat2, rename_users={"J": ["John"]})
    assert isinstance(chat.df, pd.DataFrame)


def test_rename_users():
    chat = WhatsAppChat.from_source(filename)
    chat = chat.rename_users(mapping={"J": ["John"]})
    assert isinstance(chat.df, pd.DataFrame)


def test_rename_users_error():
    chat = WhatsAppChat.from_source(filename)
    with pytest.raises(ValueError):
        chat = chat.rename_users(mapping={"J": "John"})


def test_len():
    chat = WhatsAppChat.from_source(filename)
    assert isinstance(len(chat), int)


pokemon_filename = str(CHATS_DIR / "whatsapp" / "pokemon.txt")


def test_from_sources_without_auto_header_requires_hformat():
    """auto_header=False must be honoured per file, not silently overridden.

    Regression guard: from_sources builds a per-file list from the auto_header flag. If that flag is
    ignored and detection is always enabled, this call would quietly succeed instead of raising.
    """
    with pytest.raises(ValueError, match="hformat can't be None"):
        WhatsAppChat.from_sources([filename1, filename2], auto_header=False)


def test_from_sources_honours_explicit_hformats():
    """Passing one hformat per file must give the same result as detecting them."""
    chat_auto = WhatsAppChat.from_sources([filename1, filename2])
    chat_manual = WhatsAppChat.from_sources(
        [filename1, filename2], auto_header=False, hformat=[hformat_merge, hformat_merge]
    )
    assert chat_manual.df.equals(chat_auto.df)


def test_from_source_extra_metadata_populates_name_and_system_messages():
    """extra_metadata=True must reach the parser and split system messages out of df."""
    with pytest.warns(FutureWarning):
        chat = WhatsAppChat.from_source(filepath=pokemon_filename, extra_metadata=True)

    assert chat.name == "Pokemon Chat"
    assert len(chat.df_system) == 1
    # The system message is removed from the user-message frame.
    assert chat.name not in set(chat.df["username"])

    plain = WhatsAppChat.from_source(filepath=pokemon_filename)
    assert len(plain.df) == len(chat.df) + len(chat.df_system)


# --- #177 small known bugs -----------------------------------------------------------------


def test_to_txt_rejects_wrong_extension_with_the_right_message(tmp_path):
    """The error said .zip, which is what to_zip wants, not to_txt."""
    chat = WhatsAppChat.from_source(filename)
    with pytest.raises(ValueError, match=r"must end with \.txt"):
        chat.to_txt(str(tmp_path / "chat.csv"))


def test_to_zip_rejects_wrong_extension(tmp_path):
    chat = WhatsAppChat.from_source(filename)
    with pytest.raises(ValueError, match=r"must end with \.zip"):
        chat.to_zip(str(tmp_path / "chat.txt"))


def test_rename_users_does_not_rely_on_chained_assignment():
    """Renaming must actually take effect on the returned chat, and leave the original alone.

    The previous implementation assigned through `df[col][mask] = ...`, which writes to a temporary
    and is silently ignored under pandas copy-on-write.
    """
    chat = WhatsAppChat.from_source(filename1)
    original_users = chat.users
    assert "John" in original_users

    renamed = chat.rename_users(mapping={"J": ["John"]})

    assert "J" in renamed.users
    assert "John" not in renamed.users
    assert (renamed.df["username"] == "J").sum() == (chat.df["username"] == "John").sum()
    # The source chat is untouched.
    assert chat.users == original_users


def test_rename_users_works_under_copy_on_write(monkeypatch):
    """Renaming must survive pandas copy-on-write, which is the default from pandas 3.0.

    The previous implementation assigned through ``df[col][mask] = ...``. Under copy-on-write that
    writes to a temporary and is discarded, so rename_users silently returned an unchanged chat.
    Prerequisite for #170.
    """
    monkeypatch.setattr(pd.options.mode, "copy_on_write", True)

    chat = WhatsAppChat.from_source(filename1)
    renamed = chat.rename_users(mapping={"J": ["John"]})

    assert "J" in renamed.users
    assert "John" not in renamed.users
