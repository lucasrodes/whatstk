"""Parser utils."""


import os
import re
from datetime import datetime
from urllib.request import urlopen
from typing import Optional, TYPE_CHECKING, Tuple, List, Dict

import pandas as pd

from whatstk.utils.exceptions import RegexError, HFormatError
from whatstk.utils.utils import COLNAMES_DF
from whatstk.whatsapp.auto_header import extract_header_from_text

if TYPE_CHECKING:  # pragma: no cover
    from whatstk.whatsapp.objects import WhatsAppChat  # pragma: no cover


regex_simplifier = {
    "%Y": r"(?P<year>\d{2,4})",
    "%y": r"(?P<year>\d{2,4})",
    "%m": r"(?P<month>\d{1,2})",
    "%d": r"(?P<day>\d{1,2})",
    "%H": r"(?P<hour>\d{1,2})",
    "%I": r"(?P<hour>\d{1,2})",
    "%M": r"(?P<minutes>\d{2})",
    "%S": r"(?P<seconds>\d{2})",
    "%P": r"(?P<ampm>[AaPp].? ?[Mm].?)",
    "%p": r"(?P<ampm>[AaPp].? ?[Mm].?)",
    "%name": rf"(?P<{COLNAMES_DF.USERNAME}>[^:]*)",
}


def df_from_txt_whatsapp(
    filepath: str,
    auto_header: bool = True,
    hformat: Optional[str] = None,
    encoding: str = "utf-8",
) -> "WhatsAppChat":
    """Load chat as a DataFrame.

    Args:
        filepath (str): Path to the file. Accepted sources are:

                * Local file, e.g. 'path/to/file.txt'.
                * URL to a remote hosted file, e.g. 'http://www.url.to/file.txt'.
                * Link to Google Drive file, e.g. 'gdrive://35gKKrNk-i3t05zPLyH4_P1rPdOmKW9NZ'. The format is expected
                  to be 'gdrive://[FILE-ID]'. Note that in order to load a file from Google Drive you first need to run
                  :func:`gdrive_init <whatstk.utils.gdrive.gdrive_init>`.
        auto_header (bool, optional): Detect header automatically. If False, ``hformat`` is required.
        hformat (str, optional): :ref:`Format of the header <The header format>`, e.g.
                                    ``'[%y-%m-%d %H:%M:%S] - %name:'``. Use following keywords:

                                    - ``'%y'``: for year (``'%Y'`` is equivalent).
                                    - ``'%m'``: for month.
                                    - ``'%d'``: for day.
                                    - ``'%H'``: for 24h-hour.
                                    - ``'%I'``: for 12h-hour.
                                    - ``'%M'``: for minutes.
                                    - ``'%S'``: for seconds.
                                    - ``'%P'``: for "PM"/"AM" or "p.m."/"a.m." characters.
                                    - ``'%name'``: for the username.

                                    Example 1: For the header '12/08/2016, 16:20 - username:' we have the
                                    ``'hformat='%d/%m/%y, %H:%M - %name:'``.

                                    Example 2: For the header '2016-08-12, 4:20 PM - username:' we have
                                    ``hformat='%y-%m-%d, %I:%M %P - %name:'``.
        encoding (str, optional): Encoding to use for UTF when reading/writing (ex. 'utf-8').
                                  `List of Python standard encodings <https://docs.python.org/3/library/codecs.
                                  html#standard-encodings>`_.

    Returns:
        WhatsAppChat: Class instance with loaded and parsed chat.

    ..  seealso::

        * :func:`WhatsAppChat.from_source <whatstk.whatsapp.objects.WhatsAppChat.from_source>`
        * :func:`extract_header_from_text <whatstk.whatsapp.auto_header.extract_header_from_text>`
        * :func:`gdrive_init <whatstk.utils.gdrive.gdrive_init>`

    """
    # Read local file
    text = _str_from_txt(filepath, encoding)

    # Build dataframe
    df = _df_from_str(text, auto_header, hformat)
    return df


def generate_regex(hformat: str) -> Tuple[str, str]:
    r"""Generate regular expression from hformat.

    Args:
        hformat (str): Simplified syntax for the header, e.g. ``'%y-%m-%d, %H:%M:%S - %name:'``.

    Returns:
        str: Regular expression corresponding to the specified syntax.

    Example:
        Generate regular expression corresponding to ``'hformat=%y-%m-%d, %H:%M:%S - %name:'``.

        ..  code-block:: python

            >>> from whatstk.whatsapp.parser import generate_regex
            >>> generate_regex('%y-%m-%d, %H:%M:%S - %name:')
            ('(?P<year>\\d{2,4})-(?P<month>\\d{1,2})-(?P<day>\\d{1,2}), (?P<hour>\\d{1,2}):(?P<minutes>\\d{2}):(?
            P<seconds>\\d{2}) - (?P<username>[^:]*): ', '(?P<year>\\d{2,4})-(?P<month>\\d{1,2})-(?P<day>\\d{1,2}), (?
            P<hour>\\d{1,2}):(?P<minutes>\\d{2}):(?P<seconds>\\d{2}) - ')

    """
    items = re.findall(r"\%\w*", hformat)
    for i in items:
        hformat = hformat.replace(i, regex_simplifier[i])

    hformat = hformat + " "
    hformat_x = hformat.split("(?P<username>[^:]*)")[0]
    return hformat, hformat_x


def _str_from_txt(filepath: str, encoding: str = "utf-8") -> str:
    """Read text content as string.

    Args:
        filepath (str): Path to file. Accepted: local file, url (http://...), Google Drive file (gdrive://[file-id]).
        encoding (str, optional): Encoding to use for UTF when reading/writing (ex. ‘utf-8’).
                                  `List of Python standard encodings <https://docs.python.org/3/library/codecs.
                                  html#standard-encodings>`_.

    Raises:
        FileNotFoundError: [description]

    Returns:
        str: File content as a string.
    """
    # Read local file
    if os.path.isfile(filepath) and os.access(filepath, os.R_OK):
        with open(filepath, "r", encoding=encoding) as f:
            text = f.read()
    # Read file from URL
    elif filepath.lower().startswith("http"):
        with urlopen(filepath) as response:  # noqa
            text = response.read()
        text = text.decode(encoding)
    elif filepath.startswith("gdrive"):
        from whatstk.utils.gdrive import _load_str_from_file_id

        file_id = filepath.replace("gdrive://", "")
        text = _load_str_from_file_id(file_id)
    else:
        raise FileNotFoundError(f"File {filepath} was not found locally or remotely. Please check it exists.")
    return text


def _df_from_str(text: str, auto_header: bool = True, hformat: Optional[str] = None) -> pd.DataFrame:
    # Get hformat
    if hformat:
        # Bracket is reserved character in RegEx, add backslash before them.
        hformat = hformat.replace("[", r"\[").replace("]", r"\]")
    if not hformat and auto_header:
        hformat = extract_header_from_text(text)
        if not hformat:
            raise RuntimeError(
                "Header automatic extraction failed. Please specify the format manually by setting"
                " input argument `hformat`. Report this issue so that automatic header detection support"
                " for your header format is added: https://github.com/lucasrodes/whatstk/issues."
            )
    elif not (hformat or auto_header):
        raise ValueError("If auto_header is False, hformat can't be None.")

    # Generate regex for given hformat
    r, r_x = generate_regex(hformat=hformat)

    # Parse chat to DataFrame
    try:
        df = _parse_chat(text, r)
    except RegexError:
        raise HFormatError("hformat '{}' did not match the provided text. No match was found".format(hformat))
    df = _remove_alerts_from_df(r_x, df)

    df = _add_schema(df)
    return df


def _parse_chat(text: str, regex: str) -> pd.DataFrame:
    """Parse chat using given regex.

    Args:
        text (str) Whole log chat text.
        regex (str): Regular expression

    Returns:
        pandas.DataFrame: DataFrame with messages sent by users, index is the date the messages was sent.

    Raises:
        RegexError: When provided regex could not match the text.

    """
    result = []
    headers = list(re.finditer(regex, text))
    for i in range(len(headers)):
        try:
            line_dict = _parse_line(text, headers, i)
        except KeyError:
            raise RegexError("Could not match the provided regex with provided text. No match was found.")
        result.append(line_dict)
    df_chat = pd.DataFrame.from_records(result)
    df_chat = df_chat[[COLNAMES_DF.DATE, COLNAMES_DF.USERNAME, COLNAMES_DF.MESSAGE]]
    return df_chat


def _add_schema(df: pd.DataFrame) -> pd.DataFrame:
    """Add default chat schema to df.

    Args:
        df (pandas.DataFrame): Chat dataframe.

    Returns:
        pandas.DataFrame: Chat dataframe with correct dtypes.

    """
    df = df.astype(
        {
            COLNAMES_DF.DATE: "datetime64[ns]",
            COLNAMES_DF.USERNAME: pd.StringDtype(),
            COLNAMES_DF.MESSAGE: pd.StringDtype(),
        }
    )
    return df


def _parse_line(text: str, headers: List[str], i: int) -> Dict[str, str]:
    """Get date, username and message from the i:th intervention.

    Args:
        text (str): Whole log chat text.
        headers (list): All headers.
        i (int): Index denoting the message number.

    Returns:
        dict: i:th date, username and message.

    """
    result_ = headers[i].groupdict()
    if "ampm" in result_:
        hour = int(result_["hour"])
        mode = result_.get("ampm").lower()
        if hour == 12 and mode == "am":
            hour = 0
        elif hour != 12 and mode == "pm":
            hour += 12
    else:
        hour = int(result_["hour"])

    # Check format of year. If year is 2-digit represented we add 2000
    if len(result_["year"]) == 2:
        year = int(result_["year"]) + 2000
    else:
        year = int(result_["year"])

    if "seconds" not in result_:
        date = datetime(
            year,
            int(result_["month"]),
            int(result_["day"]),
            hour,
            int(result_["minutes"]),
        )
    else:
        date = datetime(
            year,
            int(result_["month"]),
            int(result_["day"]),
            hour,
            int(result_["minutes"]),
            int(result_["seconds"]),
        )
    username = result_[COLNAMES_DF.USERNAME]
    message = _get_message(text, headers, i)
    line_dict = {
        COLNAMES_DF.DATE: date,
        COLNAMES_DF.USERNAME: username,
        COLNAMES_DF.MESSAGE: message,
    }
    return line_dict


def _remove_alerts_from_df(r_x: str, df: pd.DataFrame) -> pd.DataFrame:
    """Try to get rid of alert/notification messages.

    Args:
        r_x (str): Regular expression to detect whatsapp warnings.
        df (pandas.DataFrame): DataFrame with all interventions.

    Returns:
        pandas.DataFrame: Fixed version of input dataframe.

    """
    df_new = df.copy()
    df_new.loc[:, COLNAMES_DF.MESSAGE] = df_new[COLNAMES_DF.MESSAGE].apply(lambda x: _remove_alerts_from_line(r_x, x))
    return df_new


def _remove_alerts_from_line(r_x: str, line_df: str) -> str:
    """Remove line content that is not desirable (automatic alerts etc.).

    Args:
        r_x (str): Regula expression to detect WhatsApp warnings.
        line_df (str): Message sent as string.

    Returns:
        str: Cleaned message string.

    """
    if re.search(r_x, line_df):
        return line_df[: re.search(r_x, line_df).start()]
    else:
        return line_df


def _get_message(text: str, headers: List[str], i: int) -> str:
    """Get i:th message from text.

    Args:
        text (str): Whole log chat text.
        headers (list): All headers.
        i (int): Index denoting the message number.

    Returns:
        str: i:th message.

    """
    msg_start = headers[i].end()
    msg_end = headers[i + 1].start() if i < len(headers) - 1 else headers[i].endpos
    msg = text[msg_start:msg_end].strip()
    return msg
