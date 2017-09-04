# First attempt at creating a highly naive flight controller
# Author: Daniel Hunter
# Date: Sep 2 2017

# Imports and setup
import smbus
import math
import Adafruit_PCA9685
from collections import defaultdict

def calculateTicks(hz, pulseInMilliseconds):
	cycle = 1000 / hz
	timePerTick = cycle / 4096
	ticks = pulseInMilliseconds / timePerTick
	return ticks

def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

def calculatePower(xAngle, yAngle):
    motors = defaultdict(int)

    # Calculate relative desired motor power based on angle imbalance
    # Scale values to be -1 to 1
    xAngle = max(min(xAngle / 10, 1), -1)
    yAngle = max(min(yAngle / 10, 1), -1)

    # Set motor values based on average axis tilt
    motors['A'] = (yAngle - xAngle) / 2
    motors['B'] = (yAngle + xAngle) / 2
    motors['C'] = motors['A'] * (-1)
    motors['D'] = motors['B'] * (-1)

    # Calculate absolute motor power based on relative
    for motor in motors:
        motors[motor] = ((motors[motor] + 1) / 4) + 1.5

    return motors

def initMotors(pwm):
    pwm.set_pwm(motorChannel['A'], 0, int(calculateTicks(50, 1)))
    pwm.set_pwm(motorChannel['B'], 0, int(calculateTicks(50, 1)))
    pwm.set_pwm(motorChannel['C'], 0, int(calculateTicks(50, 1)))
    pwm.set_pwm(motorChannel['D'], 0, int(calculateTicks(50, 1)))
    input("Press Enter to fly!")
    return

if __name__ == '__main__':

    # Power management registers
    power_mgmt_1 = 0x6b
    power_mgmt_2 = 0x6c

    motorChannel = defaultdict(int)
    motorChannel['A'] = 0
    motorChannel['B'] = 3
    motorChannel['C'] = 2
    motorChannel['D'] = 1

    pwm = Adafruit_PCA9685.PCA9685()
    pwm.set_pwm_freq(50)

    bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
    address = 0x68       # This is the address value read via the i2cdetect command

    # Now wake the 6050 up as it starts in sleep mode
    bus.write_byte_data(address, power_mgmt_1, 0)

    initMotors(pwm)

    logFile = open("flight-log.txt", "w")

    # Data loop and motor commands
    try:
        while True:
            # Get IMU data
            accel_xout = read_word_2c(0x3b)
            accel_yout = read_word_2c(0x3d)
            accel_zout = read_word_2c(0x3f)

            accel_xout_scaled = accel_xout / 16384.0
            accel_yout_scaled = accel_yout / 16384.0
            accel_zout_scaled = accel_zout / 16384.0

            # TODO Use Gyro data as well
            xRotation = get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
            yRotation = get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)

            # Set motors based on IMU data
            motors = calculatePower(xRotation, yRotation)

            pwm.set_pwm(motorChannel['A'], 0, int(calculateTicks(50, float(motors['A']))))
            pwm.set_pwm(motorChannel['B'], 0, int(calculateTicks(50, float(motors['B']))))
            pwm.set_pwm(motorChannel['C'], 0, int(calculateTicks(50, float(motors['C']))))
            pwm.set_pwm(motorChannel['D'], 0, int(calculateTicks(50, float(motors['D']))))

            buf = "%d, %d\n" % (xRotation, yRotation)
            logFile.write(buf)

    except KeyboardInterrupt:
        pass
        print("Killing all motors!")
        pwm.set_pwm(motorChannel['A'], 0, int(calculateTicks(50, 1)))
        pwm.set_pwm(motorChannel['B'], 0, int(calculateTicks(50, 1)))
        pwm.set_pwm(motorChannel['C'], 0, int(calculateTicks(50, 1)))
        pwm.set_pwm(motorChannel['D'], 0, int(calculateTicks(50, 1)))
        logFile.close()
        print("Killed all motors, closed log file.")
