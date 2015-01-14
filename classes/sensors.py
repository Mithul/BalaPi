import smbus
import time

from sensors.adxl345 import ADXL345
from sensors.l3g4200d import L3G4200D
from sensors.hmc5883l import HMC5883L


import sensors.imu as imu
from sensors.i2cutils import i2c_raspberry_pi_bus_number

bus = smbus.SMBus(i2c_raspberry_pi_bus_number())
imu_controller = imu.IMU(bus, 0x69, 0x53, 0x1e, "IMU")

if __name__ == "__main__":
    last_time=time.time()
    print last_time
    gyroYangle=0
    CFangleX=0
    DT=0.02
    while(True):

        #time.sleep(0.5)
        orientation = imu_controller.read_pitch_roll_yaw()
        print orientation[0]*180,orientation[1]*180
        print ''
        AA=0.98
        last_time=time.time()
        print ''
        #exit()

