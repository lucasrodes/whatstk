import re
import pandas as pd
from datetime import datetime


regex_simplifier = {
    '%y': '(?P<year>\d{2,4})',
    '%m': '(?P<month>\d{1,2})',
    '%d': '(?P<day>\d{1,2})',
    '%H': '(?P<hour>\d{1,2})',
    '%M': '(?P<minutes>\d{2})',
    '%S': '(?P<seconds>\d{2})',
    '%P': '(?P<ampm>[AaPp].? ?[Mm].?)',
    '%name': '(?P<username>[^:]*)'
}


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


def parse_chat(text, regex):
    """

    Args: 
        text (str) Whole log chat text.
        regex (str): Regular expression
    
    Returns:
        pandas.DataFrame: DataFrame with messages sent by users, index is the date the messages was sent.

    """
    result = []
    headers = list(re.finditer(regex, text))
    for i in range(len(headers)):
        line_dict = _parse_line(text, headers, i)
        result.append(line_dict)
    df_chat = pd.DataFrame.from_records(result, index='date')
    return df_chat[['username', 'message']]


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
    username = result_['username']
    message = _get_message(text, headers, i)
    return dict(date=date, username=username, message=message)


def remove_alerts_from_df(r_x, df):
    """Tries to get rid of alert/notification messages

    Args:
        r_x (str): Regular expression to detect whatsapp warnings.
        df (pandas.DataFrame): DataFrame with all interventions.

    Returns: 
        pandas.DataFrame: Fixed version of input dataframe.

    """
    df_new = df.copy()
    df_new.loc[:, 'message'] = df_new['message'].apply(lambda x: _remove_alerts_from_line(r_x, x))
    return df_new


def _remove_alerts_from_line(r_x, line_df):
    """Remove line content that is not desirable (automatic alerts etc.)

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