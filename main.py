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

# import matplotlib.pyplot as plt
# import seaborn as sns

from whatstk.wparser import WhatsAppChat

# from whatstk import wplot as wplt
# sns.set(style="whitegrid")

wpchat = WhatsAppChat("chats/samplechat.txt")

# Obtain the names of the users from the chat
users = wpchat.usernames
# Obtain list of days with interventions
days = wpchat.days
# Obtain number of interventions in the chat
num_interventions = wpchat.num_interventions


# Print brief summary of the retrieved data
print("\n----------------------------------")
print("Brief summary")
# Print name of users
print("\n *", len(users),"users found: ")
[print("\t", user) for user in users]
# Number of days the chat has been active
print("\n * Chat was active", len(days), "days")
# Number of interventions
print(" * Chat had", num_interventions, "interventions")
# Average number of interventions per day
int_day=num_interventions/len(days)
print(" * Chat had an average of %.2f" % int_day, "interventions/day")
# Average number of interventions per day per user
int_day_pers = int_day/len(users)
print(" * Chat had an average of %.2f" % int_day_pers, "interventions/day/person")
print("\n----------------------------------")


# Obtain DataFrame containing interventions per user per day and normalize the data
interventions_per_day = wpchat.interventions_per_day

import pandas as pd

df = pd.DataFrame.from_dict(interventions_per_day, orient='columns')
# Center each dimension
df = df.sub(df.mean(axis=1), axis=0)
# Normalize each dimension
df = df.divide(df.max(axis=1)-df.min(axis=1), axis=0)

from whatstk.learning.som import SelfOrganizingMap

# We define the number of units that we will be using. Large number leads to good global
# fit but poor local fit (low number leads to the oposite)
num_units = 5
# We choose an output space define by an array of neurons arranged in a line fashion
topology = 'line'

print(df)
som = SelfOrganizingMap(df, num_units, sigma_initial=num_units/2, num_epochs=1000,
    learning_rate_initial=1, topology=topology)

som.train()
som.print_results()
#interventions_users_days = wp.normalize_dataframe(interventions_users_days)
#print(interventions_users_days)
#wp.build_dictionary_dates(data)
# Obtain DataFrame containing interventions per user per hour
#interventions_users_hours = wp.get_intervention_table_hours(users, hours, data)

# Test SOM
# Choose number of units (for 2dgrid and 2dgrid this tells the side length)
#print("Self-Organizing Map (SOM) \n")
#num_units = int(input("- Number of units: "))
#topology = input("- Topology: ")

#S = som.self_organizing_map(wpchat., num_units, sigma_initial=num_units/2, num_epochs=1000,
    #learning_rate_initial=1, topology=topology)
#S.train()
#S.print_results()
#print("\n----------------------------------")

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
