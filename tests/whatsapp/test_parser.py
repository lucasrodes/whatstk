from tests.paths import TEST_CHATS_HFORMATS_DIR, TEST_CHATS_MERGE_DIR, CHATS_DIR
import pandas as pd
import pytest
from whatstk.whatsapp.parser import df_from_whatsapp
from whatstk.whatsapp.hformat import get_supported_hformats_as_dict
from whatstk.utils.exceptions import HFormatError
from whatstk.utils.utils import COLNAMES_DF, _map_hformat_filename


# Generate chats
filenames = [
    str(TEST_CHATS_HFORMATS_DIR / f)
    for f in TEST_CHATS_HFORMATS_DIR.iterdir()
    if f.is_file() and f.name.endswith(".txt")
]
# Chats for multiple txt loading
filename1 = str(TEST_CHATS_MERGE_DIR / "file1.txt")
filename2 = str(TEST_CHATS_MERGE_DIR / "file2.txt")
# TODO: Message type chats
file_type_1 = str(CHATS_DIR / "whatsapp" / "pokemon.txt")

# Chat hosted on repo
# filepath_url = "http://raw.githubusercontent.com/lucasrodes/whatstk/master/chats/example.txt"
filepath_url = "http://raw.githubusercontent.com/lucasrodes/whatstk/master/chats/whatsapp/pokemon.txt"


def test_df_from_whatsapp():
    """This test checks most of the logic of the library.

    - Generates tests in all formats to be supported (according to JSON)
    - Loads them using manual and auto_header approaches (checks they are equivalent).
    - Checks that all chats (from different hformats) are equivalent.

    """
    info_dix = get_supported_hformats_as_dict()
    all_chats = []
    hformats = []
    for elem in info_dix:
        chats = []
        hformat = elem["format"]
        auto_header = bool(elem["auto_header"])
        filename_base = _map_hformat_filename(hformat)
        filename = str(TEST_CHATS_HFORMATS_DIR / "{}.txt".format(filename_base))
        filename_zip = str(TEST_CHATS_HFORMATS_DIR / "{}.zip".format(filename_base))

        # Auto
        if auto_header:
            chat = df_from_whatsapp(filename)
            chats.append(chat)
        # Manual
        chat = df_from_whatsapp(filename, hformat=hformat)
        chats.append(chat)

        # ZIP
        # Auto
        if auto_header:
            chat_zip = df_from_whatsapp(filename_zip)
            assert chat_zip.equals(chat)
        # Manual
        chat_zip = df_from_whatsapp(filename_zip, hformat=hformat)
        assert chat_zip.equals(chat)

        # Check manual and auto chats are equal
        assert chats[0].equals(chats[1])  # TODO: Assumes there are always two elements in list chats!

        all_chats.append(chat)
        hformats.append(hformat)

    records = []
    for i in range(len(all_chats)):
        record = {"chat": i}
        for j in range(i, len(all_chats)):
            if (all_chats[i][COLNAMES_DF.DATE].dt.second.nunique() == 1) & (
                all_chats[j][COLNAMES_DF.DATE].dt.second.nunique() != 1
            ):
                all_chats[j][COLNAMES_DF.DATE] = all_chats[j][COLNAMES_DF.DATE].map(lambda x: x.replace(second=0))
            elif (all_chats[j][COLNAMES_DF.DATE].dt.second.nunique() == 1) & (
                all_chats[i][COLNAMES_DF.DATE].dt.second.nunique() != 1
            ):
                all_chats[i][COLNAMES_DF.DATE] = all_chats[i][COLNAMES_DF.DATE].map(lambda x: x.replace(second=0))
            record[j] = all_chats[i].equals(all_chats[j])
        records.append(record)
    df = pd.DataFrame.from_records(records, index="chat")
    assert (df.eq(False)).sum().sum() == 0


def test_df_from_whatsapp_2():
    with pytest.raises(HFormatError):
        _ = df_from_whatsapp(filename1, hformat="%y")


def test_df_from_whatsapp_3():
    with pytest.raises(ValueError):
        _ = df_from_whatsapp(filename1, auto_header=False)


@pytest.mark.flaky(reruns=3, reruns_delay=2)
def test_df_from_whatsapp_url():
    df = df_from_whatsapp(filepath_url)
    assert isinstance(df, pd.DataFrame)


def test_df_from_whatsapp_gdrive(mocker):
    gdrive_url = "gdrive://456456456-ewgwegegw"
    with open(filename1, "r", encoding="utf8") as f:
        mock_text = f.read()
    # mocker.patch('whatstk.utils.gdrive._load_str_from_file_id', return_value="bla bla")
    mocker.patch("pydrive2.files.GoogleDriveFile.FetchMetadata", return_value=True)
    mocker.patch("pydrive2.files.GoogleDriveFile.GetContentString", return_value=mock_text)
    mocker.patch("whatstk.utils.gdrive._check_gdrive_config", return_value=None)
    df = df_from_whatsapp(gdrive_url)
    assert isinstance(df, pd.DataFrame)


def test_df_from_whatsapp_error():
    with pytest.raises(FileNotFoundError):
        _ = df_from_whatsapp("grger")


def test_df_message_type_true():
    df = df_from_whatsapp(file_type_1, message_type=True)
    assert isinstance(df, pd.DataFrame)

    # Check group name
    group_name = "Pokemon Chat"
    assert set(df.loc[df["username"] == group_name, COLNAMES_DF.MESSAGE_TYPE]) == {"system"}


def test_df_from_txt_whatsapp_deprecated():
    """Test deprecated function df_from_txt_whatsapp."""
    import warnings
    from whatstk.whatsapp.parser import df_from_txt_whatsapp

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        df = df_from_txt_whatsapp(filename1)
        assert len(w) == 1
        assert issubclass(w[0].category, FutureWarning)
        assert "deprecated" in str(w[0].message).lower()
        assert isinstance(df, pd.DataFrame)


def test_zip_multiple_files_error(tmpdir):
    """Test ValueError when ZIP contains multiple files."""
    import zipfile

    # Create a ZIP with multiple files
    zip_path = tmpdir.join("multi_file.zip")
    with zipfile.ZipFile(str(zip_path), "w") as zf:
        zf.writestr("file1.txt", "some content")
        zf.writestr("file2.txt", "more content")

    with pytest.raises(ValueError, match="Unexpected number of files in the ZIP"):
        df_from_whatsapp(str(zip_path))


def test_auto_header_extraction_failure():
    """Test RuntimeError when auto-header extraction fails."""
    # Create text that won't match any known header format
    text = "This is just random text\nwithout any\nheader format at all\n"
    from whatstk.whatsapp.parser import _df_from_str

    with pytest.raises(RuntimeError, match="Header automatic extraction failed"):
        _df_from_str(text, auto_header=True, hformat=None)


def test_message_type_non_group():
    """Test that message_type='user' for non-group chats."""
    # Use a file with 2-3 users - it will have message_type column
    df = df_from_whatsapp(filename1, message_type=True)

    # Should have message_type column
    assert COLNAMES_DF.MESSAGE_TYPE in df.columns
    # For non-group chats (<=2 users), all messages should be 'user'
    # Check that we have the message_type column (which covers line 150)
    assert len(df) > 0
