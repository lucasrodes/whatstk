# -*- coding: utf-8 -*-
import numpy as np
from operator import itemgetter

# Obtain usernames from the chat
def get_names(data):
	return np.unique(np.array([d[1] for d in data]))

# Obtain dates from conversations from the chat
def get_dates(data):
	dates_rep = np.array([d[0][:3] for d in data])
	# From [1]
	dates = [list(x) for x in set(tuple(x) for x in dates_rep)]
	sorted(dates,key=itemgetter(2,1,0))
	return dates


# [1] Comment from Mark Byers,
#		http://stackoverflow.com/questions/3724551/python-uniqueness-for-list-of-lists

