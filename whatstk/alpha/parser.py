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
    '%P': '(?P<ampm>[AaPp]M)',
    '%name': '(?P<username>[^:]*)'
}


def generate_regex(hformat):
    """Generate the appropriate regular expression from simplified syntax.


    :param hformat: Simplified syntax for the header.
    :type hformat: str
    :return: Regular expression corresponding to the specified syntax.
    :rtype: str
    """
    items = re.findall(r'\%\w*', hformat)
    for i in items:
        hformat = hformat.replace(i, regex_simplifier[i])

    hformat = hformat + ' '
    hformat_x = hformat.split('(?P<username>[^:]*)')[0]
    return hformat, hformat_x


def get_message(text, headers, i):
    """Get i:th message from text.

    :param text: Whole log chat text.
    :type text: str
    :param headers: All headers.
    :type headers: list
    :param i: Index denoting the message number.
    :type i: int
    :return: i:th message.
    :rtype: str
    """
    msg_start = headers[i].end()
    msg_end = headers[i + 1].start() if i < len(headers) - 1 else headers[i].endpos
    msg = text[msg_start:msg_end].strip()
    return msg


def parse_line(text, headers, i):
    """Get date, username and message from the i:th intervention.

    :param text: Whole log chat text.
    :type text: str
    :param headers: All headers.
    :type headers: list
    :param i: Index denoting the message number.
    :type i: int
    :return: i:th date, username and message.
    :rtype: dict
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

    if 'seconds' not in result_:
        date = datetime(int(result_['year']), int(result_['month']), int(result_['day']), hour,
                        int(result_['minutes']))
    else:
        date = datetime(int(result_['year']), int(result_['month']), int(result_['day']), hour,
                        int(result_['minutes']), int(result_['seconds']))
    username = result_['username']
    message = get_message(text, headers, i)
    return dict(date=date, username=username, message=message)


def parse_chat(text, regex):
    """

    :param text: Whole log chat text.
    :type text: str
    :param regex: Regular expression
    :type regex: str
    :return:
    """
    result = []
    headers = list(re.finditer(regex, text))
    for i in range(len(headers)):
        line_dict = parse_line(text, headers, i)
        result.append(line_dict)
    df_chat = pd.DataFrame.from_records(result, index='date')
    return df_chat[['username', 'message']]


def fix_df(r_x, df):
    """Get rid of alert/notification messages

    :param r_x: Regular expression to detect whatsapp warnings.
    :type r_x: str
    :param df: DataFrame with all interventions.
    :type df: pandas.DataFrame
    :return: Fixed version of input dataframe.
    :rtype: pandas.DataFrame
    """
    df_new = df.copy()
    df_new.loc[:, 'message'] = df_new['message'].apply(lambda x: fix_line_df(r_x, x))
    return df_new


def fix_line_df(r_x, line_df):
    if re.search(r_x, line_df):
        return line_df[:re.search(r_x, line_df).start()]
    else:
        return line_df