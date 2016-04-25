import pandas as pd
from datetime import datetime
import json,sys,getopt,re
class categorize:
	fileDict = 'keys.json'
	setVals = {}
	fError = []
	fHeartbeat = []
	fFileTransfer = []
	parts= None
	allKeys = []
	filePath = ''
	hbregex = re.compile(r".*?:\s([\d+,]+).*")
	hbdict = {}
	pfregex = re.compile(r".*?Cache:([\d+]).*")
	synclogregex = re.compile(r".*?SyncLog\sEvent\s(.*?)\s.*?ConnectorId.*?(\d+).*")
	ftdict = {}
	logStats = pd.DataFrame(columns=('key','Count'))
	def __init__(self,filePath):
		self.fError.append(self.parse_error_occured) 
		self.fHeartbeat.append(self.parse_heartbeat)
		self.fFileTransfer.append(self.parse_propfind)
		self.filePath = filePath
	def common_parts(self,s):
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
		
	def parse_heartbeat(self,d,s):
			if('Heartbeats generated') in s:
				matches = self.hbregex.match(s)
				if matches:
					d['connector_ids'] = matches.group(1)
					return (True,d)
				else:
					return (False,{})
			else:
				return (False,{})
	
	def parse_propfind(self,d,s):
		if('PROPFIND') in s:
			matches =  self.pfregex.match(s)
			if matches:
				print 'propfind match found', s
				d['cache_id']= int(matches.group(1))
				d['type'] = "PROPFIND"
				key = (d['year'],d['month'],d['day'],d['hour'],d['type'],-1,d['cache_id'])
				if not key in self.ftdict:
					self.ftdict[key] = 1
				else:
					self.ftdict[key] = self.ftdict[key] + 1
				return(True,d)
		return (False,{})
	def parse_synclog(self,d,s):
		if('SyncLog') in s:
			matches = self.synclogregex.match(s)
			if matches:
				print 'synclog found'
				d['connector_id'] = int(matches.group(2))
				d['type'] = matches.group(1)
				key = (d['year'],d['month'],d['day'],d['hour'],d['type'],d['connector_id'],-1)
				if not key in self.ftdict:
					self.ftdict[key] = 1
				else:
					self.ftdict[key] = self.ftdict[key] + 1
				return(True,d)
	def parse_error_occured(self,s):
		if('server failed') in s:
			return True
		if('An error occurred') in s:
			return True
		return False
	def parse_smtp_error(self,s):
		print 'parse_smtp_error'	
	
	def is_error(self,s):
		bError = False
		for e in self.fError:
			
			if e(s):
				bError = True
				break
		
		return bError
	
	def is_heartbeat(self,d,s):
		# run functions to get hb data
		for e in self.fHeartbeat:		
			hb = e(d,s)
			# hb can have a list of connector ids, parse this list
			if hb and hb[0]:
				ids = hb[1]['connector_ids'].split(',')
				for idx in ids:
					if len(idx) > 0:
						key = (hb[1]['year'], hb[1]['month'],hb[1]['day'],hb[1]['hour'],int(idx))
				#creat new key or increment existing
				if not key in self.hbdict:
					self.hbdict[key] = 1
				else:
					self.hbdict[key] = self.hbdict[key] + 1
	
	def is_Initialize_Transfer(self,s):
		match = False
		if ('Initialize chunked transfer') in s:
			match = True
		
	def is_filetransfer(self,s):
		return False
	def is_syncmessage(self,s):
		return False

	def parseLog(self,start,end):
		with open(self.filePath,'r') as f:
			for i, line in  enumerate(f):
				#print i > start, i < end, start, i,end, line
				if i >= start and i < end:
					d = self.common_parts(line)
					if d:
						self.is_heartbeat(d,line)
						self.parse_propfind(d,line)	 
						self.parse_synclog(d,line)
		print self.hbdict
		print self.ftdict
	
	def showLog(self,start,end):
		with open(self.filePath,'r') as f:
			for i, line in enumerate(f):
				if i >= start and i < end:
					print line
	def rangeLog(self):
		x= 0
		with open(self.filePath,'r') as f:
			for i, line in enumerate(f):
				x = x +1
		print 'File contains ', x, ' lines'
def main(argv):
	parseLog = False
	showLog = False
	showRange = True
	start = 0	
	end = 0
	filePath = ""
	try:
		opts, args = getopt.getopt(argv,'rhpds:e:',["start=","end="])
	except getopt.GetoptError:
		print 'categorize.py -p -d -s <startline> -e <endline>'
	for opt, arg in opts:
		if opt == '-h':
			print 'categorize.py -p -d -s <startline -e <endline>'
			sys.exit()
		elif opt in ("-p"):
			parseLog = True
		elif opt in ("-d"):
			showLog = True
		elif opt in ("-s","--start"):
			start = int(arg)
		elif opt in ("-e","--end"):
			end = int(arg)
		elif opt in ('-r'):
			showRange = True
	if showLog and (start == 0 or end == 0):
		print "-d (display log)  requires a start and end be provided to limit the output range"
	
	c = categorize("logs.csv")
	if showLog:	
		c.showLog(start,end)
	if parseLog:
		c.parseLog(start,end)
	if showRange:
		c.rangeLog()
if __name__ == "__main__":
    main(sys.argv[1:])

		
	
