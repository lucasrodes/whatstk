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

import plotly.graph_objs as go


def vis(user_data, title):
    """

    :Example:

        >>> from whatstk.core import WhatsAppChat, interventions
        >>> from plotly.offline import plot
        >>> filename = 'path/to/samplechat.txt'
        >>> hformat = '%d/%m/%y, %H:%M - %name:'
        >>> chat = WhatsAppChat.from_txt(filename, hformat)
        >>> counts = interventions(chat, 'date', msg_length=False)
        >>> counts_cumsum = counts.cumsum()
        >>> plot(vis(counts_cumsum, 'cummulative characters sent per day'))

    :param user_data:
    :param title:
    :return:
    """
    # Create a trace
    data = []

    for username in user_data:
        trace = go.Scatter(
            x = user_data.index,
            y = user_data[username],
            showlegend=True,
            name=username,
            text=user_data.index
        )
        data.append(trace)

    layout = dict(title=title, xaxis = dict(title = 'Date'))

    return dict(data=data, layout=layout)