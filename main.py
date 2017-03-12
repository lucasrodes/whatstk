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

import sys

# import matplotlib.pyplot as plt
# import seaborn as sns

from whatstk import wparser as wp
# from whatstk import wplot as wplt
from whatstk.learning import som
# sns.set(style="whitegrid")

# Read file name and store it in the list lines
fileName = sys.argv[1]

lines = []
read = False
while(not read):
    try:
        fhand = open(fileName);
        read = True
    except :
        fileName = input("Invalid filename! Please introduce a correct name: ")

for line in fhand:
    line = line.rstrip();
    lines.append(line)

# Format the chat text, each row has the format:
# [date, user, message], where data = [day,month,year,hour,minutes]
data = wp.parse_data(lines)

# Obtain the names of the users from the chat
users = wp.get_users(data)

#  Obtain list of days with interventions
days = wp.get_days(data)

# Obtain the hours in a day
hours = wp.get_hours()



# Print brief summary of the retrieved data
print("\n----------------------------------")
print("Brief summary")
print("\n *", len(users),"users found: ")
[print("\t", user) for user in users]
print("\n * Chat was active", len(days), "days")
print(" * Chat had", len(data), "interventions")
int_day=len(data)/len(days)
print(" * Chat had an average of %.2f" % int_day, "interventions/day")
int_day_pers = int_day/len(users)
print(" * Chat had an average of %.2f" % int_day_pers, "interventions/day/person")
print("\n----------------------------------")


# Obtain DataFrame containing interventions per user per day and normalize the data
interventions_users_days = wp.get_intervention_table_days(users, days, data)
interventions_users_days = wp.normalize_dataframe(interventions_users_days)
#print(interventions_users_days)
#wp.build_dictionary_dates(data)
# Obtain DataFrame containing interventions per user per hour
#interventions_users_hours = wp.get_intervention_table_hours(users, hours, data)

# Test SOM
# Choose number of units (for 2dgrid and 2dgrid this tells the side length)
num_units = 10
S = som.self_organizing_map(interventions_users_days, num_units, sigma_initial=num_units/2, num_epochs=1000,
    learning_rate_initial=1, topology="2dgridcirc")
S.train()
S.print_results()
# print interventions_users_hours
#print("Preparing plots...")

#from pandas.tools.plotting import andrews_curves
#import pandas as pd
#plt.figure()
#andrews_curves(pd.melt(interventions_users_days), 'variable')
#print(pd.melt(interventions_users_days))
#plt.show()

# Enable LaTeX fonts
# try:
#	plt.rc('text', usetex=True)
#	plt.rc('font', family='serif')
#except Exception:
#	pass

# Plots
# General
#cp.plot_total_interventions_users(interventions_users_days)
#cp.plot_interventions_per_day(interventions_users_days)
#cp.plot_distribution_total_interventions_per_day(interventions_users_days)
#cp.plot_interventions_per_hour(interventions_users_hours)

#  Intra-user relations
#cp.chat_scatter_matrix(interventions_users_days, 'Number of interventions per day')
#cp.chat_scatter_matrix_density(interventions_users_days)
#cp.violinplot_users_days(interventions_users_days)
