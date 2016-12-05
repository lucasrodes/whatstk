# -*- coding: utf-8 -*-
import sys
import re
import format as fm
import unicodedata
import numpy as np

# Read Input, execute $ python main.py < file.in 
lines = []
for line in sys.stdin:
	lines.append(line.rstrip())

# Format the chat text, each row has the format:
#			 [[day,month,year,hour,minutes], name, message]
data = fm.create_samples(lines)

names = np.unique(np.array([d[1] for d in data]))
print names