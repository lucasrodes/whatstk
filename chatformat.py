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

import unicodedata

import numpy as np
import pandas as pd
import re
from operator import itemgetter

encoding = "utf-8"  # or iso-8859-15, or cp1252, or whatever encoding you use


# Maps the input line from string to an array of the form: [[date], username, message]
def raw2format(l, p):
    header = l[:p - 1]

    day = header[0:2]
    month = header[3:5]
    # Year can be YY or YYYY
    pattern_year = '\d{,4}, '
    py = re.compile(pattern_year)
    year = py.match(header[6:]).group()[:-2]
    year_end = py.match(header[6:]).end() + 6

    hour = header[year_end:year_end + 2]
    minute = header[year_end + 3:year_end + 5]

    d = [day, month, year, hour, minute]

    n = remove_accents(header[year_end + 8:p - 1])

    m = l[p + 1:]

    return [d, n, m]


# From raw data to a matrix where each row is in format of raw2format
def clean_data(lines):
    # Regular expression to find the header of the message
    pattern = '\d?\d.\d\d.\d{,4}, \d\d:\d\d - [^:]*:'
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
            pattern_alert_whats = '\d?\d.\d\d.\d{,4}, \d\d:\d\d -'
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


# Function from [1]
def remove_accents(byte_string):
    unicode_string = byte_string.decode(encoding)
    nfkd_form = unicodedata.normalize('NFKD', unicode_string)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])


# Obtain usernames from the chat
def get_users(data):
    return np.unique(np.array([d[1] for d in data]))


# Obtain dates from conversations from the chat
def get_days(data):
    days_rep = np.array([d[0][:3] for d in data])
    days = [list(x) for x in set(tuple(x) for x in days_rep)]  # From [2]
    days = sorted(days, key=itemgetter(2, 1, 0))
    return days


def get_hours():
    return ['0' + str(s) if len(str(s)) == 1 else str(s) for s in range(24)]


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
