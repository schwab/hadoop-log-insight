# IPython log file
x = 1000
         
with open("logs.csv","r") as r:
    for line in r:
    	t = line.split(',')
        if t[0].startswith('('):
        	print t[1], t[2], t[3], t[4]
		if x < 1:
			break;
		x -=1
         
