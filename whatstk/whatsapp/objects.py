"""Library WhatsApp objects."""

import os
import tempfile
from typing import Optional, Any
import warnings
import zipfile

import pandas as pd

from whatstk._chat import BaseChat
from whatstk.utils.chat_merge import merge_chats
from whatstk.whatsapp.parser import df_from_whatsapp


class WhatsAppChat(BaseChat):
    """Load and process a WhatsApp chat file.

    Args:
        df (pandas.DataFrame): Chat.

    Example:
        This simple example loads a chat using :func:`WhatsAppChat <WhatsAppChat>`. Once loaded, we can access its
        attribute :func:`df <WhatsAppChat.df>`, which contains the loaded chat as a DataFrame.

        ..  code-block:: python

            >>> from whatstk.whatsapp.objects import WhatsAppChat
            >>> from whatstk.data import whatsapp_urls
            >>> chat = WhatsAppChat.from_source(filepath=whatsapp_urls.POKEMON)
            >>> chat.df.head(5)
                             date     username                                            message
            0 2016-08-06 13:23:00  Ash Ketchum                                          Hey guys!
            1 2016-08-06 13:25:00        Brock              Hey Ash, good to have a common group!
            2 2016-08-06 13:30:00        Misty  Hey guys! Long time haven't heard anything fro...
            3 2016-08-06 13:45:00  Ash Ketchum  Indeed. I think having a whatsapp group nowada...
            4 2016-08-06 14:30:00        Misty                                          Definetly


        Optionally, you can use the argument `extra_metadata` to add additional metadata to the chat:

        ..  code-block:: python

            >>> chat = WhatsAppChat.from_source(filepath=whatsapp_urls.POKEMON, extra_metadata=True)
            >>> chat.name
            'Pokemon Chat'
            >>> chat.df_system
                             date                                            message
            0	2016-04-15 15:04:00	Messages and calls are end-to-end encrypted. N...
            >>> chat.df.head()
                             date     username                                            message
            0 2016-08-06 13:23:00  Ash Ketchum                                          Hey guys!
            1 2016-08-06 13:25:00        Brock              Hey Ash, good to have a common group!
            2 2016-08-06 13:30:00        Misty  Hey guys! Long time haven't heard anything fro...
            3 2016-08-06 13:45:00  Ash Ketchum  Indeed. I think having a whatsapp group nowada...
            4 2016-08-06 14:30:00        Misty                                          Definetly
    """

    def __init__(self, df: pd.DataFrame) -> None:
        """Constructor.

        Args:
            df (pandas.DataFrame): Chat.

        """
        super().__init__(df, platform="whatsapp")

    @classmethod
    def from_source(
        cls,
        filepath: str,
        extra_metadata: Optional[bool] = None,
        **kwargs: Any  # noqa: ANN401
    ) -> "WhatsAppChat":
        """Create an instance from a chat text file.

        Args:
            filepath (str): Path to the file. Accepted sources are:

                * Local file, e.g. 'path/to/file.txt' or 'path/to/file.zip' (iOS).
                * URL to a remote hosted file, e.g. 'http://www.url.to/file.txt'.
                * Link to Google Drive file, e.g. 'gdrive://35gKKrNk-i3t05zPLyH4_P1rPdOmKW9NZ'. The format is expected
                  to be 'gdrive://[FILE-ID]'. Note that in order to load a file from Google Drive you first need to run
                  :func:`gdrive_init <whatstk.utils.gdrive.gdrive_init>`.
            **kwargs: Refer to the docs from
                        :func:`df_from_whatsapp <whatstk.whatsapp.parser.df_from_whatsapp>` for details on
                        additional arguments.
            extra_metadata (bool): This is experimental. If True, additional metadata will be added to the DataFrame.
                                    This includes class attributes such as chat.name, chat.df_system (DataFrame with
                                    only system messages). Note that this attribute only works on group chats.

        Returns:
            WhatsAppChat: Class instance with loaded and parsed chat.

        ..  seealso::

            * :func:`df_from_whatsapp <whatstk.whatsapp.parser.df_from_whatsapp>`
            * :func:`WhatsAppChat.from_sources <whatstk.WhatsAppChat.from_sources>`

        """
        # Use extra metadata (label message types)
        if extra_metadata:
            warnings.warn(
                (
                    "The argument `extra_metadata` is an experimental feature that might become the default "
                    "in a future version. Set `extra_metadata=False` to keep current behavior. "
                    "The new behaviour will enables class attributes `chat.name` and `chat.df_system`. "
                    "Agian, this is very experimental, and has been mostly tested on iOS."
                ),
                FutureWarning,
                stacklevel=2,
            )
            kwargs["message_type"] = True
        elif (extra_metadata is False) or (extra_metadata is None):
            kwargs["message_type"] = False
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            df = df_from_whatsapp(filepath=filepath, **kwargs)

        return cls(df)

    @classmethod
    def from_sources(
        cls, filepaths: str, auto_header: Optional[bool] = None, hformat: Optional[str] = None, encoding: str = "utf-8"
    ) -> "WhatsAppChat":
        """Load a WhatsAppChat instance from multiple sources.

        Args:
            filepaths (list): List with filepaths.
            auto_header (bool, optional): Detect header automatically (applies to all files). If None, attempts to
                                            perform automatic header detection for all files. If False, ``hformat`` is
                                            required.
            hformat (list, optional): List with the :ref:`header format <The header format>` to be used for each file.
                                        The list must be of length equal to ``len(filenames)``. A valid header format
                                        might be '[%y-%m-%d %H:%M:%S] - %name:'.
            encoding (str): Encoding to use for UTF when reading/writing (ex. ‘utf-8’).
                             `List of Python standard encodings
                             <https://docs.python.org/3/library/codecs.html#standard-encodings>`_.

        Returns:
            WhatsAppChat: Class instance with loaded and parsed chat.

        ..  seealso::

            * :func:`WhatsAppChat.from_source <WhatsAppChat.from_source>`
            * :func:`merge_chats <whatstk.utils.chat_merge.merge_chats>`

        Example:
            Load a chat using two text files. In this example, we use sample chats (available online, see urls in
            source code :mod:`whatstk.data <whatstk.data>`).

            ..  code-block:: python

                >>> from whatstk.whatsapp.objects import WhatsAppChat
                >>> from whatstk.data import whatsapp_urls
                >>> filepath_1 = whatsapp_urls.LOREM1
                >>> filepath_2 = whatsapp_urls.LOREM2
                >>> chat = WhatsAppChat.from_sources(filepaths=[filepath_1, filepath_2])
                >>> chat.df.head(5)
                                 date        username                                            message
                0 2019-10-20 10:16:00            John        Laborum sed excepteur id eu cillum sunt ut.
                1 2019-10-20 11:15:00            Mary  Ad aliquip reprehenderit proident est irure mo...
                2 2019-10-20 12:16:00  +1 123 456 789  Nostrud adipiscing ex enim reprehenderit minim...
                3 2019-10-20 12:57:00  +1 123 456 789  Deserunt proident laborum exercitation ex temp...
                4 2019-10-20 17:28:00            John                Do ex dolor consequat tempor et ex.

        """
        dfs = []
        if auto_header is None or auto_header:
            auto_header = [True] * len(filepaths)
        else:
            auto_header = [False] * len(filepaths)
        if hformat is None:
            hformat = [None] * len(filepaths)
        for filepath, ah, hf in zip(filepaths, auto_header, hformat):
            chat = WhatsAppChat.from_source(filepath, auto_header=ah, hformat=hf, encoding=encoding)
            dfs.append(chat.df)
        df = merge_chats(dfs)
        return cls(df)

    def to_zip(self, filepath: str, hformat: Optional[str] = None, encoding: str = "utf8") -> None:
        """Export chat to a zip file.

        Usefull to export the chat to different formats (i.e. using different hformats).

        Args:
            filepath (str): Name of the file to export (must be a local path).
            hformat (str, optional): Header format. Defaults to '%y-%m-%d, %H:%M - %name:'.
            encoding (str, optional): Encoding to use for UTF when reading/writing (ex. ‘utf-8’).
                             `List of Python standard encodings
                             <https://docs.python.org/3/library/codecs.html#standard-encodings>`_.

        """
        if not filepath.endswith(".zip"):
            raise ValueError(f"filepath {filepath} must end with .zip")
        if not hformat:
            hformat = "%y-%m-%d, %H:%M - %name:"
        text = _df_to_str(self.df, hformat)
        text_filename = "_chat.txt"

        # Create a temporary directory to hold the text file
        with tempfile.TemporaryDirectory() as temp_dir:
            text_file_path = os.path.join(temp_dir, text_filename)

            # Write the string to a temporary text file
            with open(text_file_path, 'w', encoding=encoding) as text_file:
                text_file.write(text)

            # Create a zip file and add the text file to it
            with zipfile.ZipFile(filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(text_file_path, text_filename)

    def to_txt(self, filepath: str, hformat: Optional[str] = None, encoding: str = "utf8") -> None:
        """Export chat to a text file.

        Usefull to export the chat to different formats (i.e. using different hformats).

        Args:
            filepath (str): Name of the file to export (must be a local path).
            hformat (str, optional): Header format. Defaults to '%y-%m-%d, %H:%M - %name:'.
            encoding (str, optional): Encoding to use for UTF when reading/writing (ex. ‘utf-8’).
                             `List of Python standard encodings
                             <https://docs.python.org/3/library/codecs.html#standard-encodings>`_.
        """
        if not filepath.endswith(".txt"):
            raise ValueError(f"filepath {filepath} must end with .zip")
        if not hformat:
            hformat = "%y-%m-%d, %H:%M - %name:"
        text = _df_to_str(self.df, hformat)
        with open(r"{}".format(filepath), "w", encoding=encoding) as f:
            f.write(text)


def _df_to_str(df: pd.DataFrame, hformat: str) -> str:
    lines = []
    raw_lines = df.values.tolist()
    for line in raw_lines:
        date, user, text = line
        hformat = hformat.replace("%name", "{name}")
        header = date.strftime(hformat).format(name=user)
        formatted_line = "{} {}".format(header, text)
        lines.append(formatted_line)
    text = "\n".join(lines)
    return text
