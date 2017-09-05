# Functions related to controlling the motors
# Author: Daniel Hunter
# Date: Sep 4 2017

import Adafruit_PCA9685
from collections import defaultdict

class MotorController:
    def __init__(self):
        self.channel = {
            'A': 0,
            'B': 3,
            'C': 2,
            'D': 1
        }

        self.current_motor_power = defaultdict(int)

        self.pwm = Adafruit_PCA9685.PCA9685()
        self.freq = 50
        self.pwm.set_pwm_freq(self.freq)

        self.set_motors() # Initialize motors to off

    def calculatePowerAndSetMotors(self, xAngle, yAngle):
        # Calculate relative desired motor power based on angle imbalance
        # Scale values to be -1 to 1
        xAngle = max(min(xAngle / 10, 1), -1)
        yAngle = max(min(yAngle / 10, 1), -1)

        # Set motor values based on average axis tilt
        new_motor_power = {
            'A': (yAngle - xAngle) / 2,
            'B': (yAngle + xAngle) / 2,
            'C': (yAngle - xAngle) / -2, # C and D are just A and B * (-1)
            'D': (yAngle + xAngle) / -2,
        }

        # Calculate absolute motor power based on relative (absolute needs to be between 1.5-2.0)
        for motor in new_motor_power:
            new_motor_power[motor] = ((new_motor_power[motor] + 1) / 4) + 1.5 # TODO Clean this up

        self.set_motors(new_motor_power)

    def set_motor(self, channel, level):
        if not 1.0 <= level <= 2.0: # Level should be between 1.0 and 2.0
            print("Error in set motor, trying to set motor", channel, "to ", level)
            return
        if sufficiently_different(self.current_motor_power[channel], level):
            # print("Just set motor", channel, "to", level)
            self.pwm.set_pwm(self.channel[channel], 0, int(calcTicks(self.freq, level)))
            self.current_motor_power[channel] = level

    def set_motors(self, power={'A': 1, 'B': 1, 'C': 1, 'D': 1}):
        for channel in 'ABCD':
            self.set_motor(channel, power[channel])

def sufficiently_different(c, r): # current, requested
    delta = 0.02 # 2% difference required
    if r > c * (1 + delta) or r < c * (1 - delta):
        return True
    return False

def calcTicks(hz, pulseInMilliseconds):
	cycle = 1000 / hz
	timePerTick = cycle / 4096
	ticks = pulseInMilliseconds / timePerTick
	return ticks
