# -*- coding: utf-8 -*-
import sys
import re


def raw2format(l,p):
	d = [l[0:2], l[3:5], l[6:10], l[12:14], l[15:17]]
	n = l[20:p-1]
	m = l[p+1:]
	return [d,n,m]

def create_samples(lines):
	# Regular expression to find the header of the message
	pattern = '\d\d/\d\d/\d{,4}, \d\d:\d\d - [\w\s]*:'
	p = re.compile(pattern)
	data = []

	count_line = 0			
	# Iterate over all lines of the chat
	for line in lines:
		# Check if regular expression matches
		m = p.match(line)
		if (m != None):
			pos = m.end() # Obtain ending position of the match
			match = m.group() # String matching the pattern
			print "spotted"
			print raw2format(line,pos)
			data.append(raw2format(line,pos))
		else:
			# If user texted messages with \n!
			print count_line
			print data
			if count_line != 0:
				data[-1][2] = data[-1][2] + "\n" + line
			else:
				count_line = -1
				continue
		print data
	return data

