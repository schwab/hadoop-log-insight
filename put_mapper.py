#!/usr/bin/python

import sys
from datetime import datetime
import re

putregex = re.compile(r".*?to\s(.*?)\s")
def create_key(s):
    validLine = s.startswith('(')
    if validLine and "PerformPut" in s:
        d ={}
        parts = s.split(',')
        dt = datetime.strptime(parts[1],' %m/%d/%Y %I:%M:%S %p')
        d['year'] = dt.year
        d['month'] = dt.month
        d['day'] = dt.day
        d['hour'] = dt.hour
        d['user'] = parts[3].strip()
        parts2 = s.split(":")
        d['shareid'] = parts2[3].split(',')[0]
        matches = putregex.match(parts[4])
        d['file']= matches.group(1)
        return (d)
    else:
        return None

for line in sys.stdin:
    try:
        #items = line.split(',')
        d = create_key(line)
        if not d is None:
            print '%s,%s,%s,%s,%s,%s,%s,1' % (d['year'],d['month'],d['day'],d['hour'],d['user'],d['shareid'],d['file'])
    except:
        pass
