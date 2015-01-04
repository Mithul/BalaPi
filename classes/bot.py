from motor import Motor
import RPi.GPIO as GPIO
import time
import smbus
import sensors.imu as imuc
from sensors.i2cutils import i2c_raspberry_pi_bus_number



class Bot:

    def __init__(self, m1, m2, imu=None):
        self.motorL = m1
        self.motorR = m2
        self.imu = imu

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

    def balance(self):
        while(True):
            #time.sleep(0.2)
            orientation = self.imu.read_all()
            print 'y ', orientation[6]
            speed = 80
            if orientation[6]<0:
                self.move(-speed,0.1)
            else:
                self.move(speed,0.1)


if __name__ == "__main__":
    GPIO.cleanup()
    time.sleep(1)
    m1 = Motor(12,11)
    m2 = Motor(13,15)
    bus = smbus.SMBus(i2c_raspberry_pi_bus_number())
    imu = imuc.IMU(bus, 0x69, 0x53, 0x1e, "IMU")
    bot= Bot(m1,m2,imu)
    bot.balance()
