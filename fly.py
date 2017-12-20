# First attempt at creating a naive flight controller, using a complementary filter
# Author: Daniel Hunter
# Date: Sep 2 2017

import smbus
import math
import time
from imu.imu import IMU
from motors.motors import MotorController
import signal

motors = MotorController()
imu = IMU()
logFile = open("log.txt", "w")

def main():
    # Power management registers
    power_mgmt_2 = 0x6c # NOTE is this a useless line?

    header = ["count", "time", "rotX", "rotY", "lastX", "lastY", "gyroX", "gyroY", "motA", "motB", "motC", "motD"]

    K = 0.98
    K1 = 1 - K

    time_diff = 0.01 # Sample at 100 Hz
    counter = 0

    # Initial set up readings
    (gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, accel_scaled_x, accel_scaled_y, accel_scaled_z) = imu.read_all()

    # Create an offset that's used throughout the entire flight
    gyro_offset_x = gyro_scaled_x
    gyro_offset_y = gyro_scaled_y

    gyro_total_x = last_x - gyro_offset_x
    gyro_total_y = last_y - gyro_offset_y

    last_x = imu.get_x_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
    last_y = imu.get_y_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)

    start_time = time.time()

    # Data loop and motor commands
    while True:
        wait(counter, start_time, time_diff)
        counter += 1
        if counter >= 300:
            # print(time.time() - start_time, counter)
            break

        # TODO: Put this all in a fxn
        (gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, accel_scaled_x, accel_scaled_y, accel_scaled_z) = imu.read_all()

        gyro_scaled_x -= gyro_offset_x
        gyro_scaled_y -= gyro_offset_y

        gyro_x_delta = (gyro_scaled_x * time_diff)
        gyro_y_delta = (gyro_scaled_y * time_diff)

        gyro_total_x += gyro_x_delta
        gyro_total_y += gyro_y_delta

        rotation_x = imu.get_x_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
        rotation_y = imu.get_y_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)

        # Manually remove bias from IMU data -- this is pretty dumb
        rotation_x = rotation_x - 3.0
        rotation_y = rotation_y + 4.7

        last_x = K * (last_x + gyro_x_delta) + (K1 * rotation_x)
        last_y = K * (last_y + gyro_y_delta) + (K1 * rotation_y)

        # Set motors based on IMU data
        motors.calculate_power(last_x, last_y)
        motors.set_motors()

        # Log current data + header labels
        log_variables = [counter, time.time() - start_time, rotation_x, rotation_y, last_x, last_y, gyro_x_delta, gyro_y_delta, motors.req_pwr['A'], motors.req_pwr['B'], motors.req_pwr['C'], motors.req_pwr['D']]
        logFile.write(format_row(log_variables))
        if (counter % 15 == 0):
            logFile.write(format_row(header))

def wait(count, start_time, time_diff):
    '''Used to force a set Hz sampling rate instead of as fast as possible.'''
    while True:
        if (time.time() - start_time) >= (time_diff * count):
            # print (time.time() - start_time, ",", count)
            return

def format_row(row):
    '''Creates a string with buffered white space using the passed in list'''
    margin = 10
    pretty_row = ''
    if type(row[0]).__name__ == 'str': # Could also do a try catch here
        for item in row:
            pretty_row += ("{item: >{margin}} ").format(item=item, margin=margin)
    else:
        for item in row:
            pretty_row += ("{item: >{margin}.2f} ").format(item=item, margin=margin)
    pretty_row += "\n" # Add a new line to the end of the row
    return pretty_row

def signal_handler(signal, frame):
    '''Stops all motors and closes log file when Ctrl-C is pressed'''
    motors.motors_off()
    logFile.close()
    print("Stopped all motors, closed log file.")
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    input("Press Enter to fly!")
    main()
