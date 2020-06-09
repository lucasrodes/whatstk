"""Parser utils."""


import re
from datetime import datetime
import pandas as pd
from whatstk.utils.exceptions import RegexError, HFormatError
from whatstk.utils.utils import COLNAMES_DF
from whatstk.whatsapp.auto_header import extract_header_from_text


regex_simplifier = {
    '%Y': r'(?P<year>\d{2,4})',
    '%y': r'(?P<year>\d{2,4})',
    '%m': r'(?P<month>\d{1,2})',
    '%d': r'(?P<day>\d{1,2})',
    '%H': r'(?P<hour>\d{1,2})',
    '%I': r'(?P<hour>\d{1,2})',
    '%M': r'(?P<minutes>\d{2})',
    '%S': r'(?P<seconds>\d{2})',
    '%P': r'(?P<ampm>[AaPp].? ?[Mm].?)',
    '%p': r'(?P<ampm>[AaPp].? ?[Mm].?)',
    '%name': fr'(?P<{COLNAMES_DF.USERNAME}>[^:]*)'
}


def df_from_txt_whatsapp(filename, auto_header=True, hformat=None, encoding='utf-8'):
    """Create instance from chat log txt file hosted locally.

    Args:

        filename (str): Path to chat text file.
        auto_header (bool): Detect header automatically. If False, ``hformat`` is required.
        hformat (str): Format of the :ref:`header <The header format>`, e.g. '[%y-%m-%d %H:%M:%S] - %name:'. Use
                        following keywords:

                            - ``%y``: for year (``%Y`` is equivalent).
                            - ``%m``: for month.
                            - ``%d``: for day.
                            - ``%H``: for 24h-hour.
                            - ``%I``: for 12h-hour.
                            - ``%M``: for minutes.
                            - ``%S``: for seconds.
                            - ``%P``: for "PM"/"AM" or "p.m."/"a.m." characters.
                            - ``%name``: for the username.

                            Example 1: To the header '12/08/2016, 16:20 - username:' corresponds the `hformat`
                            '%d/%m/%y, %H:%M - %name:'.

                            Example 2: To the header '2016-08-12, 4:20 PM - username:' corresponds the `hformat`
                            '%y-%m-%d, %I:%M %P - %name:'.
        encoding (str): Encoding to use for UTF when reading/writing (ex. ‘utf-8’).
                        `List of Python standard encodings <https://docs.python.org/3/library/codecs.
                        html#standard-encodings>`_.

    Returns:
        WhatsAppChat: Class instance with loaded and parsed chat.


    ..  seealso::

        * :func:`df_from_txt <whatstk.core.df_from_txt>`
        * :func:`WhatsAppChat.from_multiple_txt <whatstk.whatsapp.WhatsAppChat.from_multiple_txt>`
        * :func:`extract_header_from_text <extract_header_from_text>`
    """
    # Read file
    with open(filename, encoding=encoding) as f:
        text = f.read()

    # Get hformat
    if hformat:
        # Bracket is reserved character in RegEx, add backslash before them.
        hformat = hformat.replace('[', r'\[').replace(']', r'\]')
    if not hformat and auto_header:
        hformat = extract_header_from_text(text)
        if not hformat:
            raise RuntimeError("Header automatic extraction failed. Please specify the format manually by setting"
                               " input argument `hformat`.")
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

    return df


def generate_regex(hformat):
    """Generate the appropriate regular expression from simplified syntax.

    Args:
        hformat (str): Simplified syntax for the header.

    Returns:
        str: Regular expression corresponding to the specified syntax.

    """
    items = re.findall(r'\%\w*', hformat)
    for i in items:
        hformat = hformat.replace(i, regex_simplifier[i])

    hformat = hformat + ' '
    hformat_x = hformat.split('(?P<username>[^:]*)')[0]
    return hformat, hformat_x


def _parse_chat(text, regex):
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
        line_dict = _parse_line(text, headers, i)
        result.append(line_dict)
    if len(result) > 0:
        df_chat = pd.DataFrame.from_records(result, index=COLNAMES_DF.DATE)
        df_chat = df_chat[[COLNAMES_DF.USERNAME, COLNAMES_DF.MESSAGE]]
        df_chat = _add_schema(df_chat)
        return df_chat
    else:
        raise RegexError("Could not match the provided regex with provided text. Not match was found.")


def _add_schema(df):
    """Add default chat schema to df.

    Args:
        df (pandas.DataFrame): Chat dataframe.

    Returns:
        pandas.DataFrame: Chat dataframe with correct dtypes.

    """
    df = df.astype({
        COLNAMES_DF.USERNAME: pd.StringDtype(),
        COLNAMES_DF.MESSAGE: pd.StringDtype()
    })
    return df


def _parse_line(text, headers, i):
    """Get date, username and message from the i:th intervention.

    Args:
        text (str): Whole log chat text.
        headers (list): All headers.
        i (int): Index denoting the message number.

    Returns:
        dict: i:th date, username and message.

    """
    result_ = headers[i].groupdict()
    if 'ampm' in result_:
        hour = int(result_['hour'])
        mode = result_.get('ampm').lower()
        if hour == 12 and mode == 'am':
            hour = 0
        elif hour != 12 and mode == 'pm':
            hour += 12
    else:
        hour = int(result_['hour'])

    # Check format of year. If year is 2-digit represented we add 2000
    if len(result_['year']) == 2:
        year = int(result_['year']) + 2000
    else:
        year = int(result_['year'])

    if 'seconds' not in result_:
        date = datetime(year, int(result_['month']), int(result_['day']), hour,
                        int(result_['minutes']))
    else:
        date = datetime(year, int(result_['month']), int(result_['day']), hour,
                        int(result_['minutes']), int(result_['seconds']))
    username = result_[COLNAMES_DF.USERNAME]
    message = _get_message(text, headers, i)
    line_dict = {
        COLNAMES_DF.DATE: date,
        COLNAMES_DF.USERNAME: username,
        COLNAMES_DF.MESSAGE: message
    }
    return line_dict


def _remove_alerts_from_df(r_x, df):
    """Try to get rid of alert/notification messages.

    Args:
        r_x (str): Regular expression to detect whatsapp warnings.
        df (pandas.DataFrame): DataFrame with all interventions.

    Returns:
        pandas.DataFrame: Fixed version of input dataframe.

    """
    df_new = df.copy()
    df_new.loc[:, COLNAMES_DF.MESSAGE] = df_new[COLNAMES_DF.MESSAGE].apply(lambda x: _remove_alerts_from_line(r_x, x))
    df_new = _add_schema(df_new)
    return df_new


def _remove_alerts_from_line(r_x, line_df):
    """Remove line content that is not desirable (automatic alerts etc.).

    Args:
        r_x (str): Regula expression to detect WhatsApp warnings.
        line_df (str): Message sent as string.

    Returns:
        str: Cleaned message string.

    """
    if re.search(r_x, line_df):
        return line_df[:re.search(r_x, line_df).start()]
    else:
        return line_df


def _get_message(text, headers, i):
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