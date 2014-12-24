import RPi.GPIO as GPIO
import time
print 'starting'
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.output(11,True)
print 'forward?'
time.sleep(4)
GPIO.output(11,False)
GPIO.output(13,True)
print 'what ?'
time.sleep(4)
GPIO.output(13,False)
GPIO.output(11,True)
print 'reverse'
time.sleep(4)
GPIO.cleanup()
