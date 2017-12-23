# First attempt at creating a naive flight controller, using a complementary filter
# Author: Daniel Hunter
# Date: Sep 2 2017

import smbus
import math
import time
from quad import Quadcopter
import signal

quad = Quadcopter()
num_cycles = 100
counter = 0

def main():
    # Power management registers
    # power_mgmt_2 = 0x6c # NOTE is this a useless line?

    # Write the initial column names to the telemetry log
    quad.log_file.write(format_row(quad.header))

    # Initial set up readings
    quad.imu.take_initial_readings()

    # Data loop and motor commands
    while True:
        quad.wait(counter, start_time)
        counter += 1
        if counter > num_cycles:
            break

        quad.imu.take_continuous_readings()

        # Set motors based on IMU data
        quad.motors.calculate_power(quad.imu.last_x, quad.imu.last_y)
        quad.motors.set_motors()

        # Log current data
        quad.log_file.write(quad.format_row(quad.log_variables))

    # End of while loop, end flight
    quad.end_flight()

def signal_handler(signal, frame):
    '''Stops all motors and closes log file when Ctrl-C is pressed'''
    quad.end_flight()
    print("Stopped all motors, closed log file.")
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    input("Press Enter to fly!")
    main()
