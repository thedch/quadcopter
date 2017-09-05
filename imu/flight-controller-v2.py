# First attempt at creating a highly naive flight controller, using a complementary filter
# Author: Daniel Hunter
# Date: Sep 2 2017

import smbus
import math
import time
from imu import IMU
from motors import MotorController
import signal

motors = MotorController()
imu = IMU()
logFile = open("flight-log.txt", "w")

def main():
    # Power management registers
    power_mgmt_2 = 0x6c # TODO is this a useless line?

    K = 0.98
    K1 = 1 - K

    time_diff = 0.01 # Sample at 100 Hz
    counter = 1

    # Initial set up readings
    (gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, accel_scaled_x, accel_scaled_y, accel_scaled_z) = imu.read_all()

    last_x = imu.get_x_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
    last_y = imu.get_y_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)

    gyro_offset_x = gyro_scaled_x
    gyro_offset_y = gyro_scaled_y

    gyro_total_x = (last_x) - gyro_offset_x
    gyro_total_y = (last_y) - gyro_offset_y

    start_time = time.time()

    # Data loop and motor commands
    while True:
        wait(counter, start_time, time_diff)
        counter += 1
        if counter >= 300:
            print(time.time() - start_time, counter)
            break

        (gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, accel_scaled_x, accel_scaled_y, accel_scaled_z) = imu.read_all()

        gyro_scaled_x -= gyro_offset_x
        gyro_scaled_y -= gyro_offset_y

        gyro_x_delta = (gyro_scaled_x * time_diff)
        gyro_y_delta = (gyro_scaled_y * time_diff)

        gyro_total_x += gyro_x_delta
        gyro_total_y += gyro_y_delta

        rotation_x = imu.get_x_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
        rotation_y = imu.get_y_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)

        last_x = K * (last_x + gyro_x_delta) + (K1 * rotation_x)
        last_y = K * (last_y + gyro_y_delta) + (K1 * rotation_y)

        # Set motors based on IMU data
        motor_speed = motors.calculatePowerAndSetMotors(rotation_x, rotation_y)

        buf = "%d: %d, %d | %d, %d\n" % (counter, rotation_x, rotation_y, last_x, last_y)
        logFile.write(buf)

def wait(count, start_time, time_diff):
    '''Used to force a set Hz sampling rate instead of as fast as possible. Will probably be removed eventually.'''
    while True:
        if (time.time() - start_time) >= (time_diff * count):
            # print (time.time() - start_time, ",", count)
            return

def signal_handler(signal, frame):
    '''Stops all motors and closes log file when Ctrl-C is pressed'''
    motors.set_motors()
    logFile.close()
    print("Stopped all motors, closed log file.")
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    input("Press Enter to fly!")
    main()
