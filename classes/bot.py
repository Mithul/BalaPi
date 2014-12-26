from motor import Motor
import RPi.GPIO as GPIO
import time

class Bot:

	def __init__(self, m1, m2):
		self.motorL = m1
		self.motorR = m2

	def move(self,speed,s):
		self.motorL.move(speed,s)
		self.motorR.move(speed,s)
		time.sleep(s)


GPIO.cleanup()
time.sleep(5)
m1 = Motor(11,15)
m2 = Motor(13,12)

b= Bot(m1,m2)

speed=100

while speed>=-100:
	if(speed>-20 and speed<20):
		b.move(-100,0.5)
		speed = -20
	b.move(speed,1)
	print speed
	speed=speed-20

