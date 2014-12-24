import RPi.GPIO as GPIO
import time



print 'starting'
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.output(13,False)

led = GPIO.PWM(11, 100)
speed = 0
led.start(speed)

while speed <= 100:
	led.ChangeDutyCycle(speed)
	time.sleep(1)
	speed = speed + 10


led.stop()

GPIO.output(11,False)
GPIO.cleanup()
