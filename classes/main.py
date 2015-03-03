import multiprocessing
import time,smbus
from motor import Motor
import RPi.GPIO as GPIO
from bot import Bot
from sensors.i2cutils import i2c_raspberry_pi_bus_number
import sensors.imu as imuc
import sys,tty,termios
from key import _Getch


def worker(bot):
    try:
        bot[0].balance2()
    except IOError, e:
        m1.move(0,0)
        m2.move(0,0)

queue = multiprocessing.Queue()
GPIO.cleanup()
time.sleep(1)
m1 = Motor(11,12)
m2 = Motor(15,13)
bus = smbus.SMBus(i2c_raspberry_pi_bus_number())
imu = imuc.IMU(bus, 0x69, 0x53, 0x1e, "IMU")
bot= Bot(m1,m2,imu,queue)

refbot = []
refbot.append(bot)

p = multiprocessing.Process(target=worker, args=(refbot,))

p.start()
inkey = _Getch()
i=0
PID = {'PID':[1.0,0.0,0.0],'gyro':False}
queue.put(PID)
while True:
    PID = {'PID':[1.0,0.0,0.0],'gyro':False}
    PID['PID'][0]=raw_input()
    if PID['PID'][0]=='':
        PID['PID']=None
        PID['gyro']=True
        queue.put(PID)
        continue
    PID['PID'][1]=raw_input()
    PID['PID'][2]=raw_input()
    PID['gyro']=None
    print 'Change',PID
    queue.put(PID)
    # Wait for the
    # worker to finish
queue.close()
queue.join_thread()
p.join()
