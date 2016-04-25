#!/usr/bin/python

import sys
from datetime import datetime
import re

def create_key(s):
    validLine = s.startswith('(')
    if validLine and "Heartbeats" in s:
        d ={}
        parts = s.split(',')
        dt = datetime.strptime(parts[1],' %m/%d/%Y %I:%M:%S %p')
        d['year'] = dt.year
        d['month'] = dt.month
        d['day'] = dt.day
        d['hour'] = dt.hour
        parts2 = s.split(":")
        p2Data = parts2[3]
        connectors = p2Data.split(',')
        return (d,connectors[0:len(connectors)-2])
    else:
        return None

for line in sys.stdin:
    try:
        #items = line.split(',')
        d,c = create_key(line)
        if not d is None:
            for s in c:
                print '%s,%s,%s,%s,%s,1' % (d['year'],d['month'],d['day'],d['hour'],s)
    except:
        pass
