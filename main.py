# -*- coding: utf-8 -*-
import sys
import re
import chatformat as cf
import chatanalytics as ca
import unicodedata
import numpy as np
import pandas as pd

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

# Obtain interventions per day of names[0]
interventions_per_day_sb = np.zeros(len(dates))

# Obtain table with number of interventions per user per date
current_date = dates[0]
index = 0

for name in names[:1]:
	interventions = get_interventions_user(name, data)
index = 0
for i in range(len(dates)):
	[interventions_per_day_sb[i], index] = number_interv_per_day(dates[i], 
		interventions[index:])


#for i in range(len(interventions_of_sb)):
#	if (data[i][0][:3] == current_date):
#		interventions_per_day[-1] += 1
#	else:
#		interventions_per_day.append(1)
#		current_date = data[i][0][:3] 

def get_interventions_user(username_, data_):
	return [d for d in data if d[1] == username_]

def number_interv_per_day(date_, interv_):
	s = [1 if i[0][:3] == date_ else 0 for i in interv_]
	if s[-1] == 0:
		i = s.index(0)
	else:
		i = -1
	return [sum(s), i]

