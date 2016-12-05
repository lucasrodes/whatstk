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
# Obtain the dates 
dates = ca.get_dates(data)

# Obtain DataFrame containing interventions per user per date
interventions = ca.get_intervention_table(names, dates, data)

print "Preparing plots..."

# Enable LaTeX fonts
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

# Plot scatter plot between all users
p = pd.tools.plotting.scatter_matrix(interventions, alpha=0.2, figsize=(6, 6), diagonal='kde')
plt.suptitle(r'Number of interventions per day', fontsize=18)
plt.show()

# Number of interventions per user
interventions_per_user = interventions.sum(axis=0)
interventions_per_user.sort_values(inplace=True, ascending=False)
interventions_per_user.plot(kind='bar')
plt.title(r'Number of interventions per user')
plt.show()

# Number of interventions per date
interventions_per_date = interventions.sum(axis=1)
interventions_per_date.plot(kind='line')
# Apply Savitzky–Golay filter
filt_interventions_per_date = signal.savgol_filter(interventions_per_date,15,2)
plt.plot(filt_interventions_per_date,color='red')
plt.title(r'Number of interventions per day')
plt.show()

sns.distplot(interventions_per_date,bins=25)
plt.title('PDF estimation of the interventiosn per day')
plt.show()
