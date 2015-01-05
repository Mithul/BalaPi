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
        orientation = imu_controller.read_all()
        print 'pitch ', orientation[0]
        print 'roll ', orientation[1]
        print 'gyro_scaled_x ', orientation[2]
        print 'gyro_scaled_y ', orientation[3]
        print 'gyro_scaled_z ', orientation[4]
        print 'accel_scaled_x ', orientation[5]
        print 'accel_scaled_y ', orientation[6]
        print 'accel_scaled_z ',orientation[7]
        print 'raw gyro y ',orientation[8]
        print ''
        gyroYangle+=orientation[3]*DT;
        accelAngle = orientation[6]*90
        AA=0.98
        CFangleX=AA*(CFangleX + gyroYangle) +(1 - AA) * accelAngle;
        print 'Angle',gyroYangle,accelAngle,CFangleX
        while (time.time()-last_time<DT):
            time.sleep(0.001)
        print time.time(),last_time,time.time()-last_time
        last_time=time.time()
        print ''
        #exit()

