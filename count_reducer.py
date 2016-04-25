#!/usr/bin/env python
import sys
dtcount = {}

for line in sys.stdin:
    s = line.split(',')
    if s[0] in dtcount:
        dtcount[s[0]] = dtcount[s[0]] + 1
    else :
        dtcount[s[0]] = 1

print dtcount
