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

    def turn(self,speed,s):
        if speed>0:
            self.motorL.move(speed,s)
            self.motorR.move(-speed,s)
        else:
            self.motorL.move(speed,s)
            self.motorR.move(-speed,s)
            time.sleep(s)



