# -*- coding: utf-8 -*-
import sys
import re
import format as fm

# Read Input
lines = []
for line in sys.stdin:
	lines.append(line.rstrip())

fm.create_samples(lines)

