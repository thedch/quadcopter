# First attempt at creating a highly naive flight controller, using a complementary filter
# Author: Daniel Hunter
# Date: Sep 2 2017

import smbus
import math
import time
from imu.imu import IMU
import fly
import signal

imu = IMU()
logFile = open("test-log.txt", "w")

def main():
    # Power management registers
    # power_mgmt_2 = 0x6c # NOTE is this a useless line?

    log_variables = [counter, time.time() - start_time, rot_x, rot_y, last_x, last_y, gyro_x_delta, gyro_y_delta, motors.req_pwr['A'], motors.req_pwr['B'], motors.req_pwr['C'], motors.req_pwr['D']]
    header = ["count", "time", "rotX", "rotY", "lastX", "lastY", "gyroX", "gyroY", "motA", "motB", "motC", "motD"]
    logFile.write(format_row(header))

    K = 0.98

    time_diff = 0.25
    counter = 0

    # Initial set up readings
    (gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, accel_scaled_x, accel_scaled_y, accel_scaled_z) = imu.read_all()

    last_x = imu.get_x_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
    last_y = imu.get_y_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)

    gyro_offset_x = gyro_scaled_x
    gyro_offset_y = gyro_scaled_y

    gyro_total_x = (last_x) - gyro_offset_x
    gyro_total_y = (last_y) - gyro_offset_y

    start_time = time.time()

    # Data loop
    while True:
        fly.wait(counter, start_time, time_diff)
        counter += 1
        if counter > 5:
            motors.motors_off()
            break

        (gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, accel_scaled_x, accel_scaled_y, accel_scaled_z) = imu.read_all()

        gyro_scaled_x -= gyro_offset_x
        gyro_scaled_y -= gyro_offset_y

        gyro_x_delta = (gyro_scaled_x * time_diff)
        gyro_y_delta = (gyro_scaled_y * time_diff)

        gyro_total_x += gyro_x_delta
        gyro_total_y += gyro_y_delta

        rot_x = imu.get_x_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
        rot_y = imu.get_y_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)

        # Log current data
        logFile.write(fly.format_row(log_variables))

# def signal_handler(signal, frame):
#     '''Stops all motors and closes log file when Ctrl-C is pressed'''
#     logFile.close()
#     print("Stopped all motors, closed log file.")
#     exit(0)

signal.signal(signal.SIGINT, fly.signal_handler)
    input("Press Enter to fly!")
    main()
