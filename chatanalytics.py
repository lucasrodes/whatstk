# -*- coding: utf-8 -*-
import numpy as np
from operator import itemgetter
import pandas as pd

# Obtain usernames from the chat
def get_names(data):
	return np.unique(np.array([d[1] for d in data]))

# Obtain dates from conversations from the chat
def get_dates(data):
	dates_rep = np.array([d[0][:3] for d in data])
	# From [1]
	dates = [list(x) for x in set(tuple(x) for x in dates_rep)]
	dates = sorted(dates,key=itemgetter(2,1,0))
	return dates

# Return DataFrame with interventions of all users (columns) for all dates (rows)
def get_intervention_table(names, dates, data):
	# Put dates into nice visual format
	format_dates = nice_format_dates(dates)
	interventions_per_day = np.zeros(len(dates))

	# Loop for all names
	df = pd.DataFrame()
	for name in names:
		interventions = get_interventions_user(name, data)
		# Obtain number of interventions per each day contained in dates
		index = 0
		for i in range(len(dates)):
			[interventions_per_day[i], index] = get_number_interventions_per_day(dates[i], 
				interventions[index:])
		inter = pd.Series(interventions_per_day, index = format_dates)
		df.insert(0, name, inter)

	return df

	
# Parse ['DD','MM','YYYY'] to 'DD/MM/YYYY'
def nice_format_dates(dates):
	return [d[0]+"/"+d[1]+"/"+d[2] for d in dates]

# Obtain a list with all interventions of username_
def get_interventions_user(username_, data_):
	return [d for d in data_ if d[1] == username_]

# Return the number of interventions in the given date date_
# Returns an index referring to the position where next date begins
# in order to reduce the search in subsequent iterations
def get_number_interventions_per_day(date_, interv_):
	s = [1 if i[0][:3] == date_ else 0 for i in interv_]
	if s[-1] == 0:
		i = s.index(0)
	else:
		i = -1
	return [sum(s), i]

# [1] Comment from Mark Byers,
#		http://stackoverflow.com/questions/3724551/python-uniqueness-for-list-of-lists

