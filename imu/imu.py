# Functions related to getting data from the IMU
# Author: Daniel Hunter
# Date: Sep 4 2017

# Imports and setup
import smbus
import math
# import Adafruit_PCA9685
# from collections import defaultdict

class IMU:
    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.address = 0x68 # This is the address value read via the i2cdetect command
        power_mgmt_1 = 0x6b
        self.bus.write_byte_data(self.address, power_mgmt_1, 0) # wake the 6050 up as it starts in sleep mode
        # TODO self.measurements_dictionary for return value of read_all
        self.gyro_scale = 131.0
        self.accel_scale = 16384.0

    def read_all(self):
        raw_gyro_data = self.bus.read_i2c_block_data(self.address, 0x43, 6)
        raw_accel_data = self.bus.read_i2c_block_data(self.address, 0x3b, 6)

        gyro_scaled_x = twos_compliment((raw_gyro_data[0] << 8) + raw_gyro_data[1]) / self.gyro_scale
        gyro_scaled_y = twos_compliment((raw_gyro_data[2] << 8) + raw_gyro_data[3]) / self.gyro_scale
        gyro_scaled_z = twos_compliment((raw_gyro_data[4] << 8) + raw_gyro_data[5]) / self.gyro_scale

        accel_scaled_x = twos_compliment((raw_accel_data[0] << 8) + raw_accel_data[1]) / self.accel_scale
        accel_scaled_y = twos_compliment((raw_accel_data[2] << 8) + raw_accel_data[3]) / self.accel_scale
        accel_scaled_z = twos_compliment((raw_accel_data[4] << 8) + raw_accel_data[5]) / self.accel_scale

        return (gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, accel_scaled_x, accel_scaled_y, accel_scaled_z)

    def get_y_rotation(self, x, y, z):
        radians = math.atan2(x, dist(y,z))
        return -math.degrees(radians)

    def get_x_rotation(self, x, y, z):
        radians = math.atan2(y, dist(x,z))
        return math.degrees(radians)

def dist(a, b):
    return math.sqrt((a * a) + (b * b))

def twos_compliment(val):
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

if __name__ == '__main__':
    print("This file is not designed to be run by itself.")
    get_y_rotation(0,0,1)
