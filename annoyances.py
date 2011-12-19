import serial

class alarms:

	def first(self, state):
		if state:
			self.ser.write(chr(1))
		else:
			self.ser.write(chr(0))

	def second(self, state):
		if state:
			self.ser.write(chr(2))
		else:
			self.ser.write(chr(0))


	def third(self,state):
		print "third"

	alarmList = [first, second, third]
	ser = None
	def __init__ (self):
		try:
			self.ser = serial.Serial('/dev/ttyUSB1', baudrate=9600)
			self.ser.open()
		except:
			print "serial port not available"

	def doAlarm(self, level):
		if self.ser == None:
			print "serial port busted for level: ", level
			return
		if 0 <= level < len(self.alarmList):
			for a in self.alarmList:
				a(self, False)
			self.alarmList[level](self, True)


	def stopAllAlarms(self):
		if self.ser == None:
			print "stoppig alarms but serial port dead"
			return
		for a in self.alarmList:
			a(self, False)

