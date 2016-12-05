# -*- coding: utf-8 -*-
import sys
import re
import chatformat as cf
import chatanalytics as ca
import unicodedata
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns

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

interventions = ca.get_intervention_table(names, dates, data)


pd.tools.plotting.scatter_matrix(interventions, alpha=0.2, figsize=(6, 6), diagonal='kde')
plt.show()