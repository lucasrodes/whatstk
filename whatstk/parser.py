# -*- coding: utf-8 -*-
# whatsapp-stats
# Copyright (C) 2016  Lucas Rodés

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# This import makes Python use 'print' as in Python 3.x

#%%
from __future__ import print_function

from datetime import datetime
import re
import unicodedata

import numpy as np
import pandas as pd

from collections import defaultdict

encoding = "utf-8"  # or iso-8859-15, or cp1252, or whatever encoding you use
is12clock = False
#%%
def read_file(filename):
    """ Reads a text file and retrieves all its lines.

    :param filename: Path to the whatsapp log file.
    :type: str
    :return: List containing the content from **file**. Each element in
        the list is a line from the text in **file**.
    :rtype: list
    """
    raw_data = []
    read = False
    while not read:
        try:
            fhand = open(filename)
            read = True
        except:
            filename = input("Invalid filename! Please introduce a correct "
                             "name: ")

    for line in fhand:
        line = line.rstrip()
        raw_data.append(line)

    return raw_data
#%%
def textline_refactor(messy_message, p, date_format):
    """ Parses a line of the chat txt file into a legible format

    :param p: Position where the header (date info) of the message ends.
    :type p: int
    :param messy_message: Text line from a log file.
    :type messy_message: str
    :param date_format: The format of the date.
    :type date_format: str
    :return: Legible format of messy_message. It contains three fields:
        *   **date** (datetime): Date when a specific message was sent.
        *   **user** (str): Name of the user that sent a specific message
        *   **message** (str): , Message sent by the user.
    """

    header = messy_message[:p - 2]

    # Patterns
    pattern = {
        'd': '\d?\d[^0-9]',
        'm': '\d?\d[^0-9]',
        'y': '\d{,4}[^0-9]'
    }

    date = {}

    offset = 0
    if header[0] == '[':
        offset = 1

    # First date component
    date[date_format[0]], date0_end = _get_date_component(header, pattern[
        date_format[0]], offset)
    # Second date component
    date[date_format[1]], date1_end = _get_date_component(header, pattern[
        date_format[1]], date0_end)
    # Third date component
    date[date_format[2]], date2_end = _get_date_component(header, pattern[
        date_format[2]], date1_end)
    # Hour
    hour, hour_end = _get_date_component(header, '.\d?\d.', date2_end)
    # Minutes
    minute, minute_end = _get_date_component(header, '\d\d.', hour_end)
    # Separation
    m, sep_end = _get_date_component(header, '.*[-:\]] ', minute_end)

    # Ensure we have a 4-digit format year. We assume only dates starting in
    #  2000 year as valid
    if len(str(date['y'])) == 2:
        date['y'] += 2000
    # Change 12 clock to 24 clock!
    if is12clock:
        if 'P' in m:
            hour += 12
        if hour == 24:
            hour = 12

    # Complete date
    date = datetime(date['y'], date['m'], date['d'], hour, minute)
    # Username
    username = remove_accents(header[sep_end:])
    # Message
    message = remove_accents(messy_message[p:])  # TODO: use accents!
    # Parsed data
    parsed_data = [date, username, message]

    # py = re.compile(pattern[date_format[0]])
    # match_0 = py.match(header[offset:])
    # date[date_format[0]] = int(match_0.group()[:-1])
    # date0_end = match_0.end() + offset
    # py = re.compile(pattern[date_format[1]])
    # match_1 = py.match(header[date0_end:])
    # date[date_format[1]] = int(match_1.group()[:-1])
    # date1_end = match_1.end() + date0_end
    # py = re.compile(pattern[date_format[2]] + " ")
    # match_2 = py.match(header[date1_end:])
    # date[date_format[2]] = int(match_2.group()[:-2])
    # date_end = match_2.end() + date1_end
    # pattern_hour = '\d?\d.'
    # py = re.compile(pattern_hour)
    # hour_match = py.match(header[date_end:])
    # hour = int(hour_match.group()[:-1])
    # hour_end = hour_match.end() + date_end
    # pattern_minute = '\d\d'
    # py = re.compile(pattern_minute)
    # minute_match = py.match(header[hour_end:])
    # minute = int(minute_match.group())
    # minute_end = minute_match.end() + hour_end
    # pattern_sep = '.*[-:\]] '
    # py = re.compile(pattern_sep)
    # m = py.match(header[minute_end:])
    # sep_end = m.end() + minute_end

    return parsed_data
#%%
def _get_date_component(header, pattern, offset):
    py = re.compile(pattern)
    match_0 = py.match(header[offset:])
    try:
        component = int(match_0.group()[:-1])
    except:
        component = match_0.group()[:-1]
    component_end = match_0.end() + offset
    return component, component_end
#%%
def parse_chat(lines, regex_pattern, regex_pattern_alert, date_format):
    """ Parses the messy data from the txt chat file in a legible format.

    :param lines: List containing the chat text, the value at the i:th position
        corresponds to the i:th line from the chat txt file.
    :type lines: list
    :param regex_pattern: Regex pattern to detect the headers.
    :type regex_pattern: str
    :param regex_pattern_alert: Regex pattern to detect the headers of alert
        messages.
    :type regex_pattern_alert: str
    :param date_format: -
    :type date_format: str
    :return: List containing the chat in a legible format. In particular, data[i]
        corresponds to the i:th message and has the format given by
        textline_refactor function.
    :rtype: list
    """

    # Check if this is 12 or 24 clock
    pattern = '.* ([AaPp][Mm])( )?[-:\]]'
    global is12clock
    is12clock = bool(re.match(pattern, lines[0]))

    # Regular expression to find the header of the message of a user
    pattern = regex_pattern
    # Regular expression to find the header of a WhatsApp alert
    pattern_alert_whats = regex_pattern_alert

    p1 = re.compile(pattern)
    data = []

    # Iterate over all lines of the chat
    for line in lines:
        m1 = p1.match(line)

        if m1 is None:
            # Not a start of user message!
            p2 = re.compile(pattern_alert_whats)
            m2 = p2.match(line)

            # Continuation of previous message?
            if m2 is None:
                #  Merge continuation of messages
                data[-1][2] = data[-1][2] + "\n" + remove_accents(line)
        else:
            # Pattern found !
            pos = m1.end()  # Obtain ending position of the match
            # match = m1.group()  # String matching the pattern
            data.append(textline_refactor(line, pos, date_format=date_format))
    return data
#%%
def remove_accents(byte_string: str) -> str:
    """
    Strip accents from input String. Function from [3]
        :param byte_string: String to remove accents from
        :return: Input string without accents
    """
    return byte_string
    """
    try:
        byte_string = unicode(byte_string, 'utf-8')
    except NameError:  # unicode step not necessary in python 3
        pass
    byte_string = unicodedata.normalize('NFD', byte_string)
    byte_string = byte_string.encode('ascii', 'ignore')
    byte_string = byte_string.decode("utf-8")

    new_string = str(byte_string)

    return new_string
    """
#%%
# TODO: document
def user_interventions(chat: "WhatsAppChat", timestep: str='days', length: bool=False) -> pd.DataFrame:
    if timestep == 'days':
        return user_interventions_days(chat.parsed_chat, length)
    #elif timestep == 'hours':
    #    return user_interventions_hours(chat.parsed_chat)
    else:
        return 0
#%%
def user_interventions_days(data: list, length=False) -> pd.DataFrame:
    """
    Return DataFrame with interventions of all users (columns) for all days (rows)

    Parameters
    ----------
    data: list
        DataFrame containing the interventions of all users, including the text.

    Returns
    ----------
    df: DataFrame
        Table containing #interventions per user per each day
        :param data:
        :param length:
        :return:
    """

    dix = defaultdict(dict)

    for d in data:
        date = d[0].date()
        user = d[1]
        if length:
            dix[date][user] = dix[date].get(user, 0) + len(d[2])
        else:
            dix[date][user] = dix[date].get(user, 0) + 1

    df = pd.DataFrame.from_dict(dix, orient='index')
    df = df.fillna(0)
    return df
#%%
def user_interventions_hours(data):
    """
    Return DataFrame with interventions of all users (columns) for all days (rows)

    Parameters
    ----------
    data: DataFrame
        DataFrame containing the interventions of all users, including the text.

    Returns
    ----------
    df: DataFrame
        Table containing #interventions per user per each day
    """

    dix = defaultdict(dict)

    for d in data:
        date_with_hour = str(d[0].date()) + ' ' + str(d[0].hour)
        user = d[1]
        dix[date_with_hour][user] = dix[date_with_hour].get(user, 0) + 1

    df = pd.DataFrame.from_dict(dix, orient='index')
    df = df.fillna(0)
    return df
#%%
def week_hour_grid(chat: pd.DataFrame) -> pd.DataFrame:
    """
    Return DataFrame with interventions of all users (columns) for all days (rows)
        :param chat: DataFrame containing the interventions of all users, including the text.
        :return: DataFrame containing #interventions per user per each day and hour
    """
    weekdays = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    dix = defaultdict(dict)
    count=0
    for d in chat.parsed_chat:
        hour = (d[0].hour - 8)
        if hour < 0:
            count +=1
            day = weekdays[(d[0].weekday()-1)%7]
        else:
            day = weekdays[d[0].weekday()]
        hour = hour%24
        dix[day][hour] = dix[day].get(hour, 0) + 1

    df = pd.DataFrame.from_dict(dix, orient='index')
    df = df.fillna(0)
    df = df.reindex(index=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                    columns=list(range(0, 24)))
    print(count)
    return df
#%%
def response_matrix(chat: pd.DataFrame, ptype: str='absolute') -> pd.DataFrame:
    """
    Obtains the response matrix between users in the chat group
        :param chat: DataFrame containing the interventions of all users, including the text.
        :param ptype: Options for the response matrix (normalized, conditional probabilities etc.)
        :return: Response matrix as DataFrame
    """
    dix = defaultdict(dict)
    for user in chat.usernames:
        dix[user][user] = 0
    for i in range(1, len(chat.parsed_chat)):
        user_old = chat.parsed_chat[i-1][1]
        user_new = chat.parsed_chat[i][1]
        if user_old != user_new:
            dix[user_old][user_new] = dix[user_old].get(user_new,0) + 1

    df = pd.DataFrame.from_dict(dix)

    if ptype != 'absolute':
        df /= df.sum().sum()
        if ptype == 'joint':
            df = df
        elif ptype == 'conditional_replier':
            df = df.divide(df.sum(axis=1), axis=0)
        elif ptype == 'conditional_replied':
            df /= df.sum(axis=0)
        df = df.fillna(0)
        df *= 100

    df = df.fillna(0)
    return df
#%%
def histogram_intervention_length(chat: pd.DataFrame) -> pd.DataFrame:
    """
        Obtains the response matrix between users in the chat group
            :param chat: DataFrame containing the interventions of all users, including the text.
            :return:
        """
    dix = defaultdict(list)

    for intervention in chat.parsed_chat:
        if intervention[2] != "<Media omitted>" and len(intervention[2]) != 0:
            dix["user"].append(intervention[1])
            dix["length"].append(len(intervention[2]))
            dix["intervention"].append(intervention[2])

    return pd.DataFrame(dix)
#%%
class WhatsAppChat:

    def __init__(self, filename, regex=None, regex_alert=None,
                 date_format='dmy'):
        # Set regular expressions to detect headers
        if regex is not None:
            self.regex = regex
        else:
            # self.regex = '\d?\d.\d?\d.\d{,4},? \d?\d:\d\d(:\d\d)?( )?([AaPp][Mm])?( )?[-:] [^:]*: '
            self.regex = '(\[)?\d{,4}.\d{,4}.\d{,4},? \d?\d:\d\d(:\d\d)?( )?(' \
                         '[' \
                         'AaPp][Mm])?( )?[-:\]] [^:]*: '

        if regex_alert is not None:
            self.regex_alert = regex_alert
        else:
            self.regex_alert = self.regex[:-8]

        # Store raw text
        self.raw_chat = read_file(filename)
        # Parse text to a list of lists
        self.parsed_chat = parse_chat(self.raw_chat, self.regex,
                                      self.regex_alert, date_format=date_format)

    @property
    def usernames(self):
        """
        Obtain usernames from the chat

        Returns
        ----------
        list
            list with the usernames in the chat.
        """
        return np.unique(np.array([d[1] for d in self.parsed_chat]))

    @property
    def days(self):
        """
        Obtain dates from conversations from the chat

        Returns
        ----------
        days: list
            list with the days there has been any conversation in the chat
        """
        return np.unique([d[0].date() for d in self.parsed_chat])

    @property
    # TODO: implement real
    def hours(self):
        """
        Obtain the hours in a day

        Returns
        ----------
        list
            list with the hours in a day
        """

        return [s for s in range(24)]

    @property
    def num_interventions(self):
        """
        Number of interventions in a chat
        :return: integer value
        """
        return len(self.parsed_chat)

    def to_df(self):
        return pd.DataFrame(self.parsed_chat, columns=['Date', 'Username',
                                                       'Message'])

    def export_csv(self, filename, sep=',', encoding='utf-8'):
        """
        Converts the pandas DataFrame into a CSV file

        Parameters
        ----------
        filename: string
            Name of the stored CSV file
        sep: string
            Separator in the CSV file
        encoding: string
            Encoding used to store the string content
        """
        self.to_df().to_csv(filename, sep=sep, encoding=encoding)

# TODO: RETHING LOOP AS IN THE ONE ABOVE
'''def get_intervention_table_hoursday(users, hours, data):
    """
"""Return DataFrame with interventions of all users (columns) for all hour times (rows)

    Parameters
    ----------
    users: list
        List with the usernames of the chat.
    hours: list
        Hours the chat has been active.
    data: list
        Legible data.

    Returns
    ----------
    df: Dataframe
        Table containing #interventions per user per each hour of the day
    """
"""
    interventions_per_hour = np.zeros(len(hours))

    # Loop for all users
    df = pd.DataFrame()
    for user in users:
        interventions = get_interventions_user(user, data)
        # Obtain number of interventions per each day contained in hours
        for i in range(len(hours)):
            interventions_per_hour[i] = get_number_interventions_per_hour(hours[i],
                                                                          interventions)
        inter = pd.Series(interventions_per_hour, index=hours)
        df.insert(0, user, inter)

    return df


def get_list_interventions_user(username, data):
    """
    Obtains a list with all interventions of username_

    Parameters
    ----------
    username_: list
        Days the chat has been active.
    data_: list
        Legible data.

    Returns
    ----------
    list
        List of dates (nicely written) the chat has been active
    """
    return [d for d in data if d[1] == username]


def get_number_interventions_per_day(day_, interv_):
    """
    Obtains the number of interventions in the day 'day_'

    Parameters
    ----------
    day_: list
        Day we are examining.
    interv_: list
        List containing all considered interventions.

    Returns
    ----------
    list
        List containing two parameters. The first one quantifies the number
        of interventions in day 'day_'. The second one is just the index of
        the last intervention in 'day_' to make the overall search more
        efficient
    """

    s = [1 if i[0][:3] == day_ else 0 for i in interv_]
    if s[-1] == 0:
        i = s.index(0)
    else:
        i = -1
    return [sum(s), i]



def get_number_interventions_per_hour(hour_, interv_):
    """
    Obtains the number of interventions during the hour 'hour_'

    Parameters
    ----------
    hour_: list
        Hour we are examining.
    interv_: list
        List containing all considered interventions.

    Returns
    ----------
    int
        quantifies the number of interventions during 'hour_'.
    """
    s = [1 if i[0][3] == hour_ else 0 for i in interv_]
    return sum(s)
'''

"""
REFERENCES
----------

[1] MiniQuark comment,
http://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-in-a-python-unicode-string

[2] Comment from Mark Byers,
http://stackoverflow.com/questions/3724551/python-uniqueness-for-list-of-lists

[3] Function from Jer42
http://stackoverflow.com/a/31607735
"""
