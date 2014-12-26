import RPi.GPIO as GPIO
import time

class Motor:

	def __init__(self, pin1, pin2):
		self.pin1 = pin1
		self.pin2 = pin2
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(pin1,GPIO.OUT)
		GPIO.setup(pin2,GPIO.OUT)
		self.driverF = GPIO.PWM(pin1, 100)
		self.driverR = GPIO.PWM(pin2, 100)

	def forward(self,speed,s):
		self.driverR.stop()
		self.driverF.start(speed)

	def reverse(self,speed,s):
		self.driverF.stop()
		self.driverR.start(speed)
	
	def move(self,speed,s):
		if(speed>0):
			self.forward(speed,s)
		else:
			self.reverse(-speed,s)

	def __exit__(self, type, value, traceback):
        	self.driverF.stop()
		self.driverF.stop()
		GPIO.cleanup()	




