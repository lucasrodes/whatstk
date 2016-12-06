# -*- coding: utf-8 -*-
import sys
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import chatformat as cf
import chatplot as cp
import seaborn as sns

sns.set(style="whitegrid")

# Read Input, execute $ python main.py < file.in 
lines = []
for line in sys.stdin:
	lines.append(line.rstrip())

# Format the chat text, each row has the format:
#			 [[day,month,year,hour,minutes], user, message]
data = cf.clean_data(lines)


# Obtain the names of the users from the chat
users = cf.get_users(data)
# Obtain list of days with interventions
days = cf.get_days(data)
# Obtain the hours in a day
hours = cf.get_hours()

# Obtain DataFrame containing interventions per user per day
interventions_users_days = cf.get_intervention_table_days(users, days, data)
# Obtain DataFrame containing interventions per user per hour 
interventions_users_hours = cf.get_intervention_table_hours(users, hours, data)

#print interventions_users_hours
print "Preparing plots..."

# Enable LaTeX fonts
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

# Plots
# General
cp.plot_total_interventions_users(interventions_users_days)
cp.plot_interventions_per_day(interventions_users_days)
cp.plot_distribution_total_interventions_per_day(interventions_users_days)
cp.plot_interventions_per_hour(interventions_users_hours)


# Intra-user relations
cp.chat_scatter_matrix(interventions_users_days, 'Number of interventions per day')
cp.chat_scatter_matrix_density(interventions_users_days)
cp.violinplot_users_days(interventions_users_days)


