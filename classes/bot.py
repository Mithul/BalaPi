from motor import Motor
import RPi.GPIO as GPIO
import time
import smbus
import sensors.imu as imuc
import math
from sensors.i2cutils import i2c_raspberry_pi_bus_number



class Bot:

    def __init__(self, m1, m2, imu=None):
        self.motorL = m1
        self.motorR = m2
        self.imu = imu
        self.speed = 0

    def move(self,speed,s):
        if speed == self.speed:
            return
        if s==0:
            self.motorL.move(speed,s)
            self.motorR.move(speed,s)
            return
        time_inc = s/math.fabs(speed - self.speed)
        if time_inc<0.01:
            time_inc=0.001
        elif time_inc>1:
            time_inc=0.001
        while (speed > 0 and self.speed < speed) or (speed < 0 and self.speed > speed):
            if speed > 0 and self.speed < speed:
                self.speed=self.speed+5
            elif speed < 0 and self.speed > speed:
                self.speed=self.speed-5
            self.motorL.move(self.speed,s)
            self.motorR.move(self.speed,s)
            print self.speed,time_inc
            time.sleep(time_inc)

    def turn(self,speed,s):
        self.speed=0
        if speed>0:
            self.motorL.move(speed,s)
            self.motorR.move(-speed,s)
        else:
            self.motorL.move(speed,s)
            self.motorR.move(-speed,s)
            time.sleep(s)

    def balance(self):
        speed = 80
        while(True):
            #time.sleep(0.2)
            orientation = self.imu.read_all()
            threshold = 0.1
            direction = 0
            t=0.5
            if orientation[6]<-threshold:
                direction=-1
                if speed<96:
                    speed=speed+4
                self.move(-speed,t)
            elif orientation[6]>threshold:
                direction=1
                if speed<96:
                    speed=speed+4
                self.move(speed,t)
            else:
                if speed>30:
                    speed=speed-2
                if direction>0:
                    self.move(speed,t)
                elif direction<0:
                    self.move(-speed,t)
            time.sleep(0.1)
            print 'y ', orientation[6],' speed ',speed

    def balance2(self):
        KI=1
        KD=0
        KP=1
        iTerm=0
        lastAngle=0
        last_time=time.time()
        gyroYangle=0
        CFangleY=0
        DT=0.02
        while True:
            orientation = self.imu.read_all()
            gyroYangle+=orientation[3]*DT;
            accelAngle = orientation[6]*90
            AA=0.98
            CFangleY=AA*(CFangleY + gyroYangle) +(1 - AA) * accelAngle;
            Pterm = KP * CFangleY
            iTerm += KI * CFangleY
            dTerm = KD *  (CFangleY -  lastAngle)
            lastAngle = CFangleY
            print 'PID',Pterm,iTerm,dTerm
            output = Pterm + iTerm + dTerm
            speed = 0 + abs(output)*100/90
            adaptive_speed = abs(output)*speed/output
            if output==0:
                output=1
            self.move(adaptive_speed,0)
            print 'Angle',gyroYangle,accelAngle,CFangleY,output,'   ',speed,adaptive_speed
            while (time.time()-last_time<DT):
                time.sleep(0.001)
            print time.time(),last_time,time.time()-last_time
            last_time=time.time()
            print ''


if __name__ == "__main__":
    GPIO.cleanup()
    time.sleep(1)
    m1 = Motor(12,11)
    m2 = Motor(13,15)
    bus = smbus.SMBus(i2c_raspberry_pi_bus_number())
    imu = imuc.IMU(bus, 0x69, 0x53, 0x1e, "IMU")
    bot= Bot(m1,m2,imu)
    bot.balance2()
