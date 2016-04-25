#!/usr/bin/env python

import sys
from datetime import datetime


def create_key(s):
    validLine = s.startswith('(')
    if validLine:
        d ={}
        parts = s.split(',')
        dt = datetime.strptime(parts[1],' %m/%d/%Y %I:%M:%S %p')
        d['year'] = dt.year
        d['month'] = dt.month
        d['day'] = dt.day
        d['hour'] = dt.hour
        return d
    else:
        return None

for line in sys.stdin:
    #items = line.split(',')
    d =create_key(line)
    if not d is None:
        print '%s:%s:%s:%s,1' % (d['year'],d['month'],d['day'],d['hour'])
