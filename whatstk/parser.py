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
from __future__ import print_function

from datetime import datetime
import re
import unicodedata

import numpy as np
import pandas as pd

from collections import defaultdict

encoding = "utf-8"  # or iso-8859-15, or cp1252, or whatever encoding you use
is12clock = False


def read_chat(filename):
    """
    reads a chat file and stores it as X
    :param filename:
    :return:
    """
    raw_data = []
    read = False
    while not read:
        try:
            fhand = open(filename)
            read = True
        except:
            filename = input("Invalid filename! Please introduce a correct name: ")

    for line in fhand:
        line = line.rstrip()
        raw_data.append(line)

    return raw_data


def raw2format(messy_message, p):
    """
    Parses a line of the chat txt file into a legible format

    Parameters
    ----------
    messy_message: String
        String content of a line of the chat
    p: int
        Denotes the position where the header (date info) of the message ends

    Returns
    -------
    parsed_data: list
        Legible format for the message messy_message. In particular, it is
        structured as [date, user, message], where:
            * date is a list with the format [day, month, year, hour, minutes]
              containing the information of the date the message was sent
              (list of integers).
            * user is the name of the user that sent the message (string).
            * message is the messatge itself (string).
    """

    header = messy_message[:p - 2]

    # day
    pattern_day = '\d?\d.'
    py = re.compile(pattern_day)
    day = int(py.match(header).group()[:-1])
    day_end = py.match(header).end()

    # month
    pattern_month = '\d?\d.'
    py = re.compile(pattern_month)
    month = int(py.match(header[day_end:]).group()[:-1])
    month_end = py.match(header[day_end:]).end() + day_end

    # Year can be YY or YYYY
    pattern_year = '\d{,4},? '
    py = re.compile(pattern_year)
    year = int(py.match(header[month_end:]).group()[:-2])
    year_end = py.match(header[month_end:]).end() + month_end

    # Ensure we have a 4-digit format year. We assume only dates starting in 2000 year as valid
    if len(str(year)) == 2:
        year += 2000

    # Hour
    pattern_hour = '\d?\d.'
    py = re.compile(pattern_hour)
    hour = int(py.match(header[year_end:]).group()[:-1])
    hour_end = py.match(header[year_end:]).end() + year_end

    # Minute
    pattern_minute = '\d\d'
    py = re.compile(pattern_minute)
    minute = int(py.match(header[hour_end:]).group())
    minute_end = py.match(header[hour_end:]).end() + hour_end

    # Do not care about seconds

    # Separation
    pattern_sep = '.*[-:] '
    py = re.compile(pattern_sep)
    m = py.match(header[minute_end:])
    sep_end = m.end() + minute_end

    # Change 12 clock to 24 clock!
    if is12clock:
        if 'P' in m.group():
            hour += 12
        if hour == 24:
            hour = 12

    # Complete date
    date = datetime(year, month, day, hour, minute)

    # Name
    name = remove_accents(header[sep_end:])

    # Message
    message = remove_accents(messy_message[p:])

    # Parsed data
    parsed_data = [date, name, message]

    return parsed_data


def parse_chat(lines, regex_pattern, regex_pattern_alert):
    """
    Parses the messy data from the txt chat file in a legible format

    Parameters
    ----------
    lines: list
        List containing the chat text, the value at the i:th position
        corresponds to the i:th line from the chat txt file

    Returns
    -------
    data: list
        List containing the chat in a legible format. In particular, data[i]
        corresponds to the i:th message and has the format given by raw2format
        function.
    """

    # Check if this is 12 or 24 clock
    pattern = '.* ([AaPp][Mm])?( )?[-:]'
    global is12clock
    is12clock = bool(re.match(pattern, lines[0]))

    # Regular expression to find the header of the message of a user
    pattern = regex_pattern
    # Regular expression to find the header of a whatsapp alert
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
                #  Merge continuation of messages
                data[-1][2] = data[-1][2] + "\n" + remove_accents(line)
        else:
            # Pattern found !
            pos = m1.end()  # Obtain ending position of the match
            # match = m1.group()  # String matching the pattern
            data.append(raw2format(line, pos))

    return data


def remove_accents(byte_string):
    """
    Strip accents from input String. Function from [3]

    Parameters
    ----------
    byte_string: String
        The input string.

    Returns
    ----------
    new_string: String
        The processed String.
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


def get_users(data):
    """
    Obtain usernames from the chat

    Parameters
    ----------
    data: list
        Legible data.

    Returns
    ----------
    list
        list with the usernames in the chat.
    """
    return np.unique(np.array([d[1] for d in data]))


def get_days(data):
    """
    Obtain dates from conversations from the chat

    Parameters
    ----------
    data: list
        Legible data.

    Returns
    ----------
    days: list
        list with the days there has been any conversation in the chat
    """
    return np.unique([d[0].date() for d in data])


def get_hours():
    """
    Obtain the hours in a day

    Returns
    ----------
    list
        list with the hours in a day
    """

    return [s for s in range(24)]


def get_intervention_table_days(data):
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
    """

    dix = defaultdict(dict)

    for d in data:
        date = d[0].date()
        user = d[1]
        dix[date][user] = dix[date].get(user, 0) + 1

    df = pd.DataFrame.from_dict(dix, orient='index')
    df = df.fillna(0)
    return df


def get_intervention_table_days_hours(data):
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
        dix[date_with_hour][user] = dix[date_with_hour].get(user,0) + 1

    df = pd.DataFrame.from_dict(dix, orient='index')
    df = df.fillna(0)
    return df


def week_hour_grid(chat):
    """
    Return DataFrame with interventions of all users (columns) for all days (rows)

    Parameters
    ----------
    chat: DataFrame
        DataFrame containing the interventions of all users, including the text.

    Returns
    ----------
    df: DataFrame
        Table containing #interventions per user per each day
    """
    weekdays = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    dix = defaultdict(dict)

    for d in chat.parsed_chat:
        hour = d[0].hour
        day = weekdays[d[0].weekday()]
        dix[day][hour] = dix[day].get(hour, 0) + 1

    df = pd.DataFrame.from_dict(dix, orient='index')
    df = df.fillna(0)
    df = df.reindex(index=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                    columns=list(range(0, 24)))
    return df


def get_response_matrix():
    return 0


# TODO: RETHING LOOP AS IN THE ONE ABOVE
"""def get_intervention_table_hoursday(users, hours, data):
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

    return df"""


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


class WhatsAppChat:

    def __init__(self, filename, regex=None, regex_alert=None):
        # Set regular expressions to detect headers
        if regex is not None:
            self.regex = regex
        else:
            self.regex = '\d?\d.\d?\d.\d{,4},? \d?\d:\d\d(:\d\d)?( )?([AaPp][Mm])?( )?[-:] [^:]*: '

        if regex_alert is not None:
            self.regex_alert = regex_alert
        else:
            self.regex_alert = self.regex[:-8]

        # Store raw text
        self.raw_chat = read_chat(filename)
        # Parse text to a list of lists
        self.parsed_chat = parse_chat(self.raw_chat, self.regex, self.regex_alert)

        # Get basic information
        self.usernames = get_users(self.parsed_chat)
        self.days = get_days(self.parsed_chat)
        self.hours = get_hours()
        self.num_interventions = len(self.parsed_chat)

        # Advanced attributes that might be removed from constructor!
        # self.interventions_per_day =

    def response_matrix_probability(self, ptype='absolute'):
        dix = defaultdict(dict)
        for user in self.usernames:
            dix[user][user] = 0
        for i in range(1,len(self.parsed_chat)):
            user_old = self.parsed_chat[i-1][1]
            user_new = self.parsed_chat[i][1]
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

    def user_interventions(self, timestep='days'):

        if timestep == 'days':
            return get_intervention_table_days(self.parsed_chat)
        elif timestep == 'hours':
            return get_intervention_table_days_hours(self.parsed_chat)
        else:
            return 0

    def to_DataFrame(self):
        return pd.DataFrame(self.parsed_chat, columns = ['Date', 'Username', 'Message'])

    def to_csv(self, filename, sep=',', encoding='utf-8'):
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
        self.to_DataFrame().to_csv(filename, sep=sep, encoding=encoding)


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
