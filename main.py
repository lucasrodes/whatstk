# -*- coding: utf-8 -*-
import sys
import re
import chatformat as cf
import chatanalytics as ca
import unicodedata
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy as sp
from scipy import signal

# Read Input, execute $ python main.py < file.in 
lines = []
for line in sys.stdin:
	lines.append(line.rstrip())

# Format the chat text, each row has the format:
#			 [[day,month,year,hour,minutes], name, message]
data = cf.create_samples(lines)

# Obtain the names of the users from the chat
names = ca.get_names(data)
# Obtain the days 
days = ca.get_days(data)
# Obtain the hours
hours = ca.get_hours()

# Obtain DataFrame containing interventions per user per date
interventions_days = ca.get_intervention_table_days(names, days, data)
interventions_hours = ca.get_intervention_table_hours(names, hours, data)



print "Preparing plots..."

# Enable LaTeX fonts
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

# Plot scatter plot between all users
p = pd.tools.plotting.scatter_matrix(interventions_days, alpha=0.2, figsize=(6, 6), diagonal='kde')
plt.suptitle(r'Number of interventions per day', fontsize=18)
plt.show()

# Number of interventions per user
interventions_days_user = interventions_days.sum(axis=0)
interventions_days_user.sort_values(inplace=True, ascending=False)
interventions_days_user.plot(kind='bar')
plt.title(r'Number of interventions per user')
plt.show()

# Number of interventions per date
interventions_days_day = interventions_days.sum(axis=1)
interventions_days_day.plot(kind='line')
# Apply Savitzky–Golay filter
filt_interventions_per_date = signal.savgol_filter(interventions_days_day,15,2)
plt.plot(filt_interventions_per_date,color='red')
plt.title(r'Number of interventions per day')
plt.show()

sns.distplot(interventions_days_day,bins=25)
plt.title('PDF estimation of the interventiosn per day')
plt.show()
