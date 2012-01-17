import sys
import socket
import urllib, urllib2

'''
annoyances.py
Things to annoy people with.

Each function is in the table-o-annoyances and is called with the doAlarm method
THESE WILL NEED EDITING FOR YOUR CONFIGURATION. All of these are specific to our network
'''
class alarms:
	#change the status of our traffic light
	def sendTraffic(self, lev):
		if 0 <= lev < 4:
			message = urllib.quote("$rage" + str(lev))
			urllib2.urlopen("http://babbage:8020/%s" % message)
		else:
			print "invalid level"

	#first annoyance
	def first(self, state):
		if state:
			self.sendTraffic(1)	
			self.ircSpeak("The sink has stuff in it")
		else:
			self.sendTraffic(0)	

	#second annoyance
	def second(self, state):
		if state:
			self.sendTraffic(2)
			self.ircSpeak("The sink *still* has washing up in it")	
		else:
			self.sendTraffic(0)	

	#third annoyance
	def third(self,state):
		if state:
			self.sendTraffic(3)	
			self.ircSpeak("FFS the sink needs cleaning, someone sort it out!")
		else:
			self.sendTraffic(0)	

	#build a function list to call from doAlarm
	alarmList = [first, second, third]
	
	def __init__ (self):
		#I used to ping things to the serial port until I decided that the traffic lights were a better idea
		print "serial port not available, using IRC and traffic lights"
	
	#send a string through IRC, this depends on our network setup so will need rewriting for yours
	def ircSpeak(self, text):
		sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sc.connect(("babbage",12345))
		sc.send(text)
		sc.close()

	#trigger an alarm, first stop all other alarms, then start our requested one
	def doAlarm(self, level):
		if 0 <= level < len(self.alarmList):
			for a in self.alarmList:
				a(self, False)
			self.alarmList[level](self, True)

	#cycle through all alarm methods and run the "stop" command
	def stopAllAlarms(self):
		for a in self.alarmList:
			a(self, False)
		#the next line got annoying
#		self.ircSpeak("The sink has been cleared, happy days")

