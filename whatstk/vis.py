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

import seaborn as sns
import matplotlib.pyplot as plt


# Visualize Response Matrix
def response_matrix(response_matrix, ptype='absolute', title_size=20, xlabel_size=12, ylabel_size=12, tick_size=8, anot_size=8, cmap='RdYlGn_r'):

    title = 'Response Matrix: '
    fmt = '.2f'
    if ptype == 'absolute':
        title += 'Number of responses'
    elif ptype == 'joint':
        title += 'P(replied, replier)'
    elif ptype == 'conditional_replier':
        title += 'P(replied | replier)'
    elif ptype == 'conditional_replied':
        title += 'P(replier | replied)'

    ax = sns.heatmap(response_matrix, annot=True, fmt=fmt, annot_kws={"size": anot_size}, cbar=False, cmap=cmap)
    labels = [m.replace(' ', '\n') if len(m.split(' ')) > 1 else m for m in response_matrix.columns]

    ax.axes.set_title(title,fontsize=title_size)
    ax.set_xlabel("Replied", fontsize=xlabel_size)
    ax.set_ylabel("Replier", fontsize=ylabel_size)
    ax.tick_params(labelsize=tick_size)

    ax.set_xticklabels(labels)
    ax.set_yticklabels(labels[::-1])
    plt.yticks(rotation=0)

    plt.show()


# Visualize Response Matrix
def week_hour_grid(week_hour_grid, ptype='absolute', title_size=20, xlabel_size=12, ylabel_size=12, tick_size=8, anot_size=8, cmap='RdYlGn_r'):

    title = 'Week Hour Activity Grid'
    fmt = 'g'

    ax = sns.heatmap(week_hour_grid, annot=True, fmt=fmt, annot_kws={"size": anot_size}, cmap=cmap, cbar=False)

    ax.axes.set_title(title, fontsize=title_size)
    ax.set_xlabel("Hours", fontsize=xlabel_size)
    ax.set_ylabel("Days", fontsize=ylabel_size)
    ax.tick_params(labelsize=tick_size)

    sns.plt.yticks(rotation=0)

    sns.plt.show()


def temporal_data(dataframe, title):
    sns.set_style("ticks")
    NUM_COLORS = len(list(dataframe))

    cm = plt.get_cmap('gist_rainbow')
    fig = plt.figure()
    #ax = fig.add_subplot(111)
    #ax.set_color_cycle([cm(1. * i / NUM_COLORS) for i in range(NUM_COLORS)])

    plt.plot(dataframe, color=[cm(1. * i / NUM_COLORS) for i in range(NUM_COLORS)])
    plt.title(title, fontsize=20)
    plt.xlabel("Time (days)", fontsize=15)
    plt.legend(list(dataframe), fontsize=15)
    plt.grid()
    plt.show()
