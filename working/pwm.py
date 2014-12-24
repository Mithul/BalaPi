import RPi.GPIO as GPIO
import time



print 'starting'
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.output(13,False)

led = GPIO.PWM(11, 100)
led2 = GPIO.PWM(13, 100)
speed = 100
led.start(speed)

while speed > 20:
	led.ChangeDutyCycle(speed)
	time.sleep(0.5)
	speed = speed - 20
	print speed


led.stop()

GPIO.output(11,False)


led2.start(100)
time.sleep(0.5)

while speed <= 100:
	led2.ChangeDutyCycle(speed)
	time.sleep(0.5)
	speed = speed + 20
	print speed


led.stop()


GPIO.output(11,False)
GPIO.cleanup()
