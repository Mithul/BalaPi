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
    bot[0].balance2()

queue = multiprocessing.Queue()
GPIO.cleanup()
time.sleep(1)
m1 = Motor(12,11)
m2 = Motor(13,15)
bus = smbus.SMBus(i2c_raspberry_pi_bus_number())
imu = imuc.IMU(bus, 0x69, 0x53, 0x1e, "IMU")
bot= Bot(m1,m2,imu,queue)

refbot = []
refbot.append(bot)

p = multiprocessing.Process(target=worker, args=(refbot,))

p.start()
inkey = _Getch()
i=0
PID = [0.0,0.0,0.0]
while True:
    PID[0]=raw_input()
    queue.put(PID)
    # Wait for the
    # worker to finish
queue.close()
queue.join_thread()
p.join()
