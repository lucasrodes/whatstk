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
from operator import itemgetter

import numpy as np
import pandas as pd

encoding = "utf-8"  # or iso-8859-15, or cp1252, or whatever encoding you use
is12clock = False

# TODO: VERY SENSITIVE TO DIFFERENT DAYS/MONTH FORMATS
# TODO Specify that the format [[date], username, message] is that of the output
# Maps the input line from string to an array of the form: [[date], username, message]
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
    pattern_year = '\d{,4}, '
    py = re.compile(pattern_year)
    year = int(py.match(header[month_end:]).group()[:-2])
    year_end = py.match(header[month_end:]).end() + month_end

    # Hour
    pattern_hour = '\d?\d.'
    py = re.compile(pattern_hour)
    hour = int(py.match(header[year_end:]).group()[:-1])
    hour_end = py.match(header[year_end:]).end() + year_end

    # Minute
    pattern_minute = '\d\d.'
    py = re.compile(pattern_minute)
    minute = int(py.match(header[hour_end:]).group()[:-1])
    minute_end = py.match(header[hour_end:]).end() + hour_end

    # Do not care about seconds

    # Separation
    pattern_sep = '.*[-:] '
    py = re.compile(pattern_sep)
    sep_end = py.match(header[minute_end:]).end() + minute_end

    # Change 12 clock to 24 clock!
    if(is12clock):
        if(header[sep_end-4] == 'P'):
            hour += 12
        if(hour%12 == 0):
            hour -= 12

    # Complete date
    date = [day, month, year, hour, minute]

    # Name
    name = remove_accents(header[sep_end:])

    # Message
    message = messy_message[p:]

    # Parsed data
    parsed_data = [date, name, message]

    return parsed_data


def parse_data(lines):
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
    pattern = '.* ([AP]M)[-:]'
    global is12clock
    is12clock = bool(re.match(pattern, lines[0]))

    # Regular expression to find the header of the message
    pattern = '\d?\d.\d\d.\d{,4}, \d?\d:\d\d(:\d\d)? ([AP]M)?[-:] [^:]*: '
    # pattern = '\d?\d.\d\d.\d{,4}, \d?\d:\d\d(:\d\d)? ([AP]M)?[(-):] [^:]*:'
    p1 = re.compile(pattern)
    data = []

    # Iterate over all lines of the chat
    for line in lines:
        m1 = p1.match(line)
        if m1 is not None:
            # Pattern found !
            # Remove accents from previous message
            try:
                data[-1][2] = remove_accents(data[-1][2])
            except Exception:
                pass

            pos = m1.end()  # Obtain ending position of the match
            match = m1.group()  # String matching the pattern
            data.append(raw2format(line, pos))
        else:
            # Pattern not found! Continuation of previous message or WhatsApp alert?
            # Regular expression to detect WhatsApp alert
            pattern_alert_whats = '\d?\d.\d\d.\d{,4}, \d?\d:\d\d(:\d\d)? ([AP]M)?[-:]'
            #pattern_alert_whats = '\d?\d.\d\d.\d{,4}, \d?\d:\d\d(:\d\d)? ([AP]M)?[(-):]'
            p2 = re.compile(pattern_alert_whats)
            m2 = p2.match(line)

            if m2 is None:
                #  Merge continuation of messages
                data[-1][2] = data[-1][2] + "\n" + line

                #  Remove accents from previous message
    try:
        data[-1][2] = remove_accents(data[-1][2])
    except Exception:
        print("")

    return data


# Function from [3]
def remove_accents(byte_string):
    """
        Strip accents from input String.

        :param byte_string: The input string.
        :type byte_string: String.

        :returns: The processed String.
        :rtype: String.
        """
    try:
        byte_string = unicode(byte_string, 'utf-8')
    except NameError:  # unicode is a default on python 3
        pass
    byte_string = unicodedata.normalize('NFD', byte_string)
    byte_string = byte_string.encode('ascii', 'ignore')
    byte_string = byte_string.decode("utf-8")
    return str(byte_string)


# Obtain usernames from the chat
def get_users(data):
    return np.unique(np.array([d[1] for d in data]))


# Obtain dates from conversations from the chat
# The input data is assumed to be in the shape as
def get_days(data):
    days_rep = np.array([d[0][:3] for d in data])
    days = [list(x) for x in set(tuple(x) for x in days_rep)]  # From [2]
    days = sorted(days, key=itemgetter(2, 1, 0))
    return days


def get_hours():
    return [s for s in range(24)]
    #return ['0' + str(s) if len(str(s)) == 1 else str(s) for s in range(24)]

#def hour_12to24(hour_24):
#    d = datetime.strptime(str(hour_24), "%H:%M")
#    return d.strftime("%I:%M %p")

#def hour_24to12(hour_24):
#    d = datetime.strptime(hour_24, "%H:%M")
#    return d.strftime("%I:%M %p")

# Return DataFrame with interventions of all users (columns) for all days (rows)
def get_intervention_table_days(users, days, data):
    # Put dates into nice visual format
    format_days = nice_format_days(days)
    interventions_per_day = np.zeros(len(days))

    # Loop for all names
    df = pd.DataFrame()
    for user in users:
        interventions = get_interventions_user(user, data)
        # Obtain number of interventions per each day contained in dates
        index = 0
        for i in range(len(days)):
            [interventions_per_day[i], index] = get_number_interventions_per_day(days[i],
                                                                                 interventions[index:])
        inter = pd.Series(interventions_per_day, index=format_days)
        df.insert(0, user, inter)

    return df


# Return DataFrame with interventions of all users (columns) for all hour times (rows)
def get_intervention_table_hours(users, hours, data):
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


# Parse ['DD','MM','YYYY'] to 'DD/MM/YYYY'
def nice_format_days(days):
    return [d[0] + "/" + d[1] + "/" + d[2] for d in days]


# Obtain a list with all interventions of username_
def get_interventions_user(username_, data_):
    return [d for d in data_ if d[1] == username_]


# Return the number of interventions in the given day day_
# Returns an index referring to the position where next date begins
# in order to reduce the search in subsequent iterations
def get_number_interventions_per_day(day_, interv_):
    s = [1 if i[0][:3] == day_ else 0 for i in interv_]
    if s[-1] == 0:
        i = s.index(0)
    else:
        i = -1
    return [sum(s), i]


#  Return number of interventions in a specific hour range
def get_number_interventions_per_hour(hour_, interv_):
    s = [1 if i[0][3] == hour_ else 0 for i in interv_]
    return sum(s)

    #  REFERENCES
    #
    # [1] MiniQuark comment,
    # http://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-in-a-python-unicode-string
    #
    # [2] Comment from Mark Byers,
    # http://stackoverflow.com/questions/3724551/python-uniqueness-for-list-of-lists
    #
    # [3] Function from Jer42
    # http://stackoverflow.com/a/31607735
