# Functions related to getting data from the IMU
# Author: Daniel Hunter
# Date: Sep 4 2017

# Imports and setup
import smbus
import math
# import Adafruit_PCA9685
# from collections import defaultdict

class IMU:
    def __init__(self, sample_hz):
        self.bus = smbus.SMBus(1)
        self.address = 0x68 # This is the address value read via the i2cdetect command
        power_mgmt_1 = 0x6b
        self.bus.write_byte_data(self.address, power_mgmt_1, 0) # wake the 6050 up as it starts in sleep mode

        # TODO self.measurements_dictionary for return value of read_all
        self.gyro_scale = 131.0
        self.accel_scale = 16384.0
        self.K = 0.98
        self.sample_hz = sample_hz

        self.gyro_scaled_x = 0
        self.gyro_scaled_y = 0
        self.gyro_scaled_z = 0
        self.accel_scaled_x = 0
        self.accel_scaled_y = 0
        self.accel_scaled_z = 0

        self.gyro_offset_x = 0
        self.gyro_offset_y = 0
        self.gyro_total_x = 0
        self.gyro_total_y = 0

        self.last_x = 0
        self.last_y = 0

    def read_all(self):
        raw_gyro_data = self.bus.read_i2c_block_data(self.address, 0x43, 6)
        raw_accel_data = self.bus.read_i2c_block_data(self.address, 0x3b, 6)

        self.gyro_scaled_x = twos_compliment((raw_gyro_data[0] << 8) + raw_gyro_data[1]) / self.gyro_scale
        self.gyro_scaled_y = twos_compliment((raw_gyro_data[2] << 8) + raw_gyro_data[3]) / self.gyro_scale
        self.gyro_scaled_z = twos_compliment((raw_gyro_data[4] << 8) + raw_gyro_data[5]) / self.gyro_scale

        self.accel_scaled_x = twos_compliment((raw_accel_data[0] << 8) + raw_accel_data[1]) / self.accel_scale
        self.accel_scaled_y = twos_compliment((raw_accel_data[2] << 8) + raw_accel_data[3]) / self.accel_scale
        self.accel_scaled_z = twos_compliment((raw_accel_data[4] << 8) + raw_accel_data[5]) / self.accel_scale

    def take_initial_readings(self):
        self.read_all()

        # Set the offset
        self.gyro_offset_x = self.gyro_scaled_x
        self.gyro_offset_y = self.gyro_scaled_y

        # Update the gyro totals
        self.gyro_total_x = self.last_x - self.gyro_offset_x
        self.gyro_total_y = self.last_y - self.gyro_offset_y

        # Set the initial last_x and last_y values
        self.last_x = self.get_x_rotation(self.accel_scaled_x, self.accel_scaled_y, self.accel_scaled_z)
        self.last_y = self.get_y_rotation(self.accel_scaled_x, self.accel_scaled_y, self.accel_scaled_z)

    def take_continuous_readings(self):
        self.read_all()

        self.gyro_scaled_x -= self.gyro_offset_x
        self.gyro_scaled_y -= self.gyro_offset_y

        gyro_x_delta = (self.gyro_scaled_x * (1 / self.sample_hz))
        gyro_y_delta = (self.gyro_scaled_y * (1 / self.sample_hz))

        self.gyro_total_x += gyro_x_delta
        self.gyro_total_y += gyro_y_delta

        rotation_x = self.get_x_rotation(self.accel_scaled_x, self.accel_scaled_y, self.accel_scaled_z)
        rotation_y = self.get_y_rotation(self.accel_scaled_x, self.accel_scaled_y, self.accel_scaled_z)

        self.last_x = self.K * (self.last_x + gyro_x_delta) + (1 - self.K) * rotation_x
        self.last_y = self.K * (self.last_y + gyro_y_delta) + (1 - self.K) * rotation_y

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
    print("This file is not designed to be run alone.")
