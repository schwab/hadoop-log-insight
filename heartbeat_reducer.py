#!/usr/bin/python

import sys
dtcount = {}
def create_key(vals):
	key = str(vals[0]) + ',' + str(vals[1]) + ',' + str(vals[2]) + ',' + str(vals[3]) + ',' + str(vals[4])
	return key	

print "year,month,day,hour,connectorid,heartbeats"
for line in sys.stdin:
    try:
        s = line.split(',')
        key =create_key(s)
        if key in dtcount:
            dtcount[key] = dtcount[key] + 1
        else :
            dtcount[key] = 1
    except Value:
        pass

for x in dtcount:
    print x + ',' + str(dtcount[x])
