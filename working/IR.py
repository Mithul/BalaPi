import RPi.GPIO as GPIO

import time

print 'starting'
GPIO.setmode(GPIO.BOARD)
GPIO.setup(18,GPIO.IN)
GPIO.setup(16,GPIO.IN)

while True:
	print GPIO.input(16),GPIO.input(18)
	time.sleep(0.5)
