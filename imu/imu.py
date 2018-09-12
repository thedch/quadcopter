# Functions related to getting data from the IMU
# Author: Daniel Hunter
# Date: Sep 4 2017

import math
from Adafruit_BNO055 import BNO055

class IMU:
    def __init__(self):
        bno = BNO055.BNO055(serial_port='/dev/serial0', rst=18)

        if not bno.begin():
            raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

        status, self_test, error = bno.get_system_status()
        print('System status: {0}'.format(status))
        print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
        if status == 0x01:
            print('System error: {0}'.format(error))
            print('See datasheet section 4.3.59 for the meaning.')
            
    def read_data(self):
        heading, roll, pitch = bno.read_euler()
        sys, gyro, accel, mag = bno.get_calibration_status()
        print('Heading={0:0.2F} Roll={1:0.2F} Pitch={2:0.2F}\tSys_cal={3} Gyro_cal={4} Accel_cal={5} Mag_cal={6}'.format(
            heading, roll, pitch, sys, gyro, accel, mag))

if __name__ == '__main__':
    print("This file is not designed to be run alone.")
