# -*- coding: utf-8 -*-
import sys
import re
import numpy as np
import unicodedata

encoding = "utf-8" # or iso-8859-15, or cp1252, or whatever encoding you use

# Returns information in format [date, username and message]
def raw2format(l,p):
	header = l[:p-1]

	day = header[0:2]
	month = header[3:5]
	# Year can be YY or YYYY
	pattern_year = '\d{,4}, '
	py = re.compile(pattern_year)
	year = py.match(header[6:]).group()[:-2]
	year_end = py.match(header[6:]).end() + 6

	hour = header[year_end:year_end+2]
	minute = header[year_end+3:year_end+5]

	d = [day, month, year, hour, minute]

	n = remove_accents(header[year_end+8:p-1])
	
	m = l[p+1:]

	return [d,n,m]

# From raw data to a matrix where each row is in format of raw2format
def create_samples(lines):
	# Regular expression to find the header of the message
	pattern = '\d\d.\d\d.\d{,4}, \d\d:\d\d - [^:]*:'
	p1 = re.compile(pattern)
	data = []

	# Iterate over all lines of the chat
	for line in lines:
		m1 = p1.match(line)
		if (m1 != None):
			# Pattern found !
			
			# Remove accents from previous message
			try:
				data[-1][2] = remove_accents(data[-1][2])
			except Exception:
				pass
			
			pos = m1.end() # Obtain ending position of the match
			match = m1.group() # String matching the pattern
			data.append(raw2format(line,pos))
		else:
			# Pattern not found! Continuation of previous message or WhatsApp alert?
			# Regular expression to detect WhatsApp alert
			pattern_alert_whats = '\d\d.\d\d.\d{,4}, \d\d:\d\d -'
			p2 = re.compile(pattern_alert_whats)
			m2 = p2.match(line)
			if (m2 == None):
				# Merge continuation of messages
				data[-1][2] = data[-1][2] + "\n" + line
	
	# Remove accents from previous message
	try:
		data[-1][2] = remove_accents(data[-1][2])
	except Exception:
		print ""
	
	return data

# Function from [1]
def remove_accents(byte_string):
	unicode_string = byte_string.decode(encoding)
	nfkd_form = unicodedata.normalize('NFKD', unicode_string)
	return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

# REFERENCES 
#
# [1] MiniQuark comment,
# http://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-in-a-python-unicode-string



