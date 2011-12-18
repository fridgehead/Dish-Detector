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

	print "second alarm"

	def third(self,state):
		print "third"

	alarmList = [first, second, third]
	ser = None
	def __init__ (self):
		self.ser = serial.Serial('/dev/ttyUSB1', baudrate=9600)
		self.ser.open()
		pass

	def doAlarm(self, level):
		if 0 <= level < len(self.alarmList):
			for a in self.alarmList:
				a(self, False)
			self.alarmList[level](self, True)

		pass

	def stopAllAlarms(self):
		for a in self.alarmList:
			a(self, False)

