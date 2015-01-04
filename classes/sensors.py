import smbus
import time

import sensors.imu as imu
from sensors.i2cutils import i2c_raspberry_pi_bus_number

bus = smbus.SMBus(i2c_raspberry_pi_bus_number())
imu_controller = imu.IMU(bus, 0x69, 0x53, 0x1e, "IMU")

if __name__ == "__main__":
    while(True):
        time.sleep(0.2)
        orientation = imu_controller.read_all()
        print 'pitch ', orientation[0]
        print 'roll ', orientation[1]
        print 'gyro_scaled_x ', orientation[2]
        print 'gyro_scaled_y ', orientation[3]
        print 'gyro_scaled_z ', orientation[4]
        print 'accel_scaled_x ', orientation[5]
        print 'accel_scaled_y ', orientation[6]
        print 'accel_scaled_z ',orientation[7]
        print ''
