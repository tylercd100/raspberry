#!/usr/bin/env python

def daemonize():
	import os, sys

	if os.fork() > 0:
	    os._exit(0)

	sys.stdin = open("/dev/null", "r")
	sys.stdout = open("/dev/null", "w")
	sys.stderr = open("/dev/null", "w")

def printToFile(f,str):
	print str
	l = open(f,'a')
	l.write(str + '\n')
	l.close()

def checkTime():
	ans = False
	now = datetime.datetime.now()
	# printToFile(logFile,str(now.hour) +', '+ str(hours[0]) +', '+ str(hours[1]))
	if (now.hour >= hours[0] and now.hour < hours[1]):
	# if (now.minute % 2):
		ans = True 
	else:
		ans = False
	printToFile(logFile, str(ans))
	return ans

import datetime
import time
import serial
import MySQLdb

daemonize()

hours = 7, 21
sleeptime = 5
timeIsOk = True
prevtimeIsOk = True

_id = 0;

now = datetime.datetime.now()

logFile = '/var/log/bookshelfgarden/log.log' #+now.strftime("%Y-%m-%dT%H.%M")+'.log'

l = open(logFile,'w')
l.write('')
l.close()

printToFile(logFile,'Starting Bookshelf')
printToFile(logFile,now.strftime("%Y-%m-%d %H:%M"))
checkTime()
printToFile(logFile,'Connecting...')
while True:
	try:
		ser = serial.Serial('/dev/ttyACM'+str(_id), 9600)
	except serial.serialutil.SerialException:
		_id = _id + 1;
		if(_id >= 10):
			_id = 0
			time.sleep(2)
	else:
		printToFile(logFile,'connected to /dev/ttyACM'+str(_id))
		break;

# db = MySQLdb.connect(host="localhost", # your host, usually localhost
#                      user="root", # your username
#                       passwd="joshua22", # your password
#                       db="garden") # name of the data base

# cur = db.cursor()


#send to arduino
# printToFile(logFile,'Sending to Arduino: '+str(int(timeIsOk)))
# ser.write(str(int(timeIsOk)))

printToFile(logFile,'Sleeping for 5 seconds...')
time.sleep(5)

while True:
	try:
		while ser.inWaiting():
			# ser.flushInput()
			printToFile(logFile,'Message from Arduino:"'+ser.readline()+'"')

		timeIsOk = checkTime()
		if (timeIsOk != prevtimeIsOk): 
			now = datetime.datetime.now()
			printToFile(logFile,now.strftime("%Y-%m-%d %H:%M")+': timeIsOk changed to '+str(timeIsOk))
			prevtimeIsOk = timeIsOk
			printToFile(logFile,'Sending to Arduino: '+str(int(timeIsOk)))
			ser.write(str(int(timeIsOk)))

		time.sleep(sleeptime)
	except serial.serialutil.SerialException:
		ser.close()
		printToFile(logFile,'Lost connection to /dev/ttyACM'+str(_id))
		printToFile(logFile,'Retrying...')
		while True:
			try:
				ser = serial.Serial('/dev/ttyACM'+str(_id), 9600)
			except serial.serialutil.SerialException:
				_id = _id + 1;
				if(_id >= 10):
					_id = 0
					time.sleep(2)
			else:
				printToFile(logFile,'connected to /dev/ttyACM'+str(_id))
				break;
	



# def readBuffer():
# 	while ser.inWaiting():
# 		msgId = ser.readline()
# 		if(msgId[:1] == 'i'):
# 			sensor = ser.readline()
# 			val = ser.readline()
# 			print msgId, sensor, val

# 			now = datetime.datetime.now()
# 			t = now.strftime("%Y-%m-%dT%H:%M:%S")

# 			# cur.execute("INSERT INTO sensors (time, sensor, value) VALUES (%s,%s,%s)",(t, sensor, val))
# 			# db.commit() 
		
# 		else:
# 			print 'idk '+msgId
# 			# print 'checking the time'
# 			# now = datetime.datetime.now()
# 			# if(now.minute % 2 == 0):
# 			# 	ser.write('1')
# 			# else:
# 			# 	ser.write('0')
