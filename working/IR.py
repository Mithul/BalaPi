import RPi.GPIO as GPIO

import time

print 'starting'
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.IN)
GPIO.setup(13,GPIO.IN)

while True:
	print GPIO.input(11),GPIO.input(13)
	time.sleep(0.5)
