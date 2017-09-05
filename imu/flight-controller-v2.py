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
    counter = 0

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
        # hold(counter, start_time, time_diff)
        counter += 1
        # print("Getting data...")
        if counter >= 1000:
            print(time.time() - start_time)
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

        buf = "%d, %d\n" % (rotation_x, rotation_y)
        logFile.write(buf)

    # print "{0:.4f} {1:.2f} {2:.2f} {3:.2f} {4:.2f} {5:.2f} {6:.2f}".format( time.time() - now, (last_x), gyro_total_x, (last_x), (last_y), gyro_total_y, (last_y))
    # print "{0:.4f} {1:.2f} {2:.2f} {3:.2f} {4:.2f} {5:.2f} {6:.2f}".format( time.time() - now, (rotation_x), (gyro_total_x), (last_x), (rotation_y), (gyro_total_y), (last_y))

def hold(count, start_time, time_diff):
    while True:
        if (time.time() - start_time) >= (time_diff * count):
            print (time.time() - start_time, ", ", count)
            return

def signal_handler(signal, frame):
    motors.set_motors()
    logFile.close()
    print("Killed all motors, closed log file.")
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    # input("Press Enter to fly!")
    main()
