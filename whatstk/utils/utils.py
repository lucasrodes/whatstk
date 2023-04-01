"""Utils."""

from typing import TYPE_CHECKING
import pandas as pd

if TYPE_CHECKING:  # pragma: no cover
    from whatstk._chat import BaseChat  # pragma: no cover


class ColnamesDf:
    """Access class constants using variable ``whatstk.utils.utils.COLNAMES_DF``.

    Example:
            Access constant ``COLNAMES_DF.DATE``:

            ..  code-block:: python

                >>> from whatstk.utils.utils import COLNAMES_DF
                >>> COLNAMES_DF.DATE
                'date'

    """

    DATE = "date"
    """Date column"""

    USERNAME = "username"
    """Username column"""

    MESSAGE = "message"
    """Message column"""

    MESSAGE_LENGTH = "message_length"
    """Message length column"""


COLNAMES_DF = ColnamesDf()


def _get_df(df: pd.DataFrame, chat: "BaseChat") -> pd.DataFrame:
    if (df is None) & (chat is None):
        raise ValueError("Please provide a chat, using either argument `df` or `chat`.")
    if (df is None) and (chat is not None):
        df = chat.df
    return df


def _map_hformat_filename(filename: str) -> str:
    """Map hformat to valid filename (Linux, MacOS, Win).

    Args:
        filename (str): Header format.

    Returns:
        str: Mapped header format.
    """
    filename = filename.replace(" ", "_").replace("/", "--").replace(":", ";")
    return filename
