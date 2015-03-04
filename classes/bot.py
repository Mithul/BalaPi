from motor import Motor
import RPi.GPIO as GPIO
import time
import smbus
import sensors.imu as imuc
import math
from sensors.i2cutils import i2c_raspberry_pi_bus_number



class Bot:

    def __init__(self, m1, m2, imu=None,queue=None):
        self.motorL = m1
        self.motorR = m2
        self.imu = imu
        self.speed = 0
        self.queue=queue
        self.offsetAngle = 0
        # Initialize input pins for the IR sensors
        GPIO.setup(18,GPIO.IN)
        GPIO.setup(16,GPIO.IN)

    def move(self,speed,s):
            '''Moves both motors with the same speed in the same direction'''
            self.motorL.move(speed,s)
            self.motorR.move(speed,s)

    def turn(self,speed,s):
        '''Moves both motors in opposite directions to turn the robot.
        Sign of the speed decides the direction of the turn'''
        self.speed=0
        if speed>0:
            self.motorL.move(speed,s)
            self.motorR.move(-speed,s)
        else:
            self.motorL.move(speed,s)
            self.motorR.move(-speed,s)
            time.sleep(s)

    def balance(self):
        '''Primitive balancing functions'''
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

    def getPIDvalues(self):
        '''Gets the PID values from the main program for live testing of PIDs'''
        try:
           return self.queue.get_nowait()
        except Exception, e:
           return None

    def detectObstacle(self):
        '''Reads the inputs from the IR sensors'''
        return {'front':GPIO.input(16),'back':GPIO.input(18)}

    def balance2(self):
        '''Main function to balance the robot'''
        #Initialize all variables
        KI=0
        KD=0
        KP=1
        iTerm=0
        lastAngle=0
        last_time=time.time()
        gyroYangle=0
        CFangleY=0
        DT=0.02
        #Open files for saving measured data for analysis
        f = open('point.txt', 'w')
        f1 = open('point1.txt', 'w')
        i=0
        while True:
            i=i+1
            #Get PID values from the main thread and set the constants and reset the zero angle
            PID = self.getPIDvalues()
            if PID is not None:
                if PID['PID'] is not None:
                    PID=PID['PID']
                    KP=float(PID[0])
                    KI= float(PID[1])
                    KD=float(PID[2])
                elif PID['gyro'] is not None:
                    self.offsetAngle=CFangleY + self.offsetAngle
                    iTerm=0
            #orientation = self.imu.read_all()
            #gyroYangle+=(orientation[8]+18)*DT/5
            #accelAngle = orientation[6]*90
            #AA=0.9
            #CFangleY=AA*(CFangleY + gyroYangle) +(1 - AA) * accelAngle;
            #Read the angle from the IMU
            CFangleY=self.imu.read_pitch_roll_yaw()[0]*180/3.14 - self.offsetAngle
            #Pterm = KP * 110*(1-1.05**(-abs(CFangleY)))*abs(CFangleY)/CFangleY
            #Detect obstacles and accordingle add an offset to the speed
            obstacle = self.detectObstacle()
            if obstacle['front']:
                oTerm=oTerm+1
            if obstacle['back']==1:
                oTerm=oTerm-1
            if obstacle['front']==0 and obstacle['back']==0:
                oTerm=0
            #Calculate the PID values from the constans and the angle
            Pterm = KP * CFangleY
            iTerm += KI * CFangleY*DT
            dTerm = KD *  (CFangleY -  lastAngle)
            lastAngle = CFangleY
            if iTerm>500:
                iTerm = 500
            elif iTerm<-500:
                iTerm = -500
            print 'PID',Pterm,iTerm,dTerm
            output = Pterm + iTerm + dTerm + oTerm
            speed = 0 + abs(output)*100/90
            if speed>100:
                speed=99.9
            if output==0:
                output=1
            adaptive_speed = abs(output)*speed/output
            self.move(adaptive_speed,0.01)
            print 'PID ',KP,KI,KD
            print 'Angle',gyroYangle,accelAngle,CFangleY,output,'   ',speed,adaptive_speed
            #Write the data to the files
            f.write(str(i)+'\t'+str(CFangleY)+'\t'+str(gyroYangle)+'\t'+str(accelAngle)+'\n')
            f1.write(str(i)+'\t'+str(Pterm)+'\t'+str(iTerm)+'\t'+str(dTerm)+'\t'+str(output)+'\t'+str(adaptive_speed)+'\n')
            #Ensures a 20ms time interval for every iteration for accurate angle reading
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
