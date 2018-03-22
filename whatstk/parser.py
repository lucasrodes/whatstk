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

import numpy as np
import pandas as pd


encoding = "utf-8"  # or iso-8859-15, or cp1252, or whatever encoding you use
is12clock = False


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
    hour, hour_end = _get_date_component(header, '\d?\d.', date2_end)
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
        if 'P' in m.group():
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


def _get_date_component(header, pattern, offset):
    py = re.compile(pattern)
    match_0 = py.match(header[offset:])
    component = int(match_0.group()[:-1])
    component_end = match_0.end() + offset
    return component, component_end


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
                #  Merge continuation of messages
                data[-1][2] = data[-1][2] + "\n" + remove_accents(line)
        else:
            # Pattern found !
            pos = m1.end()  # Obtain ending position of the match
            # match = m1.group()  # String matching the pattern
            data.append(textline_refactor(line, pos, date_format=date_format))
    return data


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
