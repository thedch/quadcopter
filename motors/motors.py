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

        self.curr_pwr = defaultdict(int)
        self.req_pwr = defaultdict(int) # Requested motor power

        self.pwm = Adafruit_PCA9685.PCA9685()
        self.freq = 50
        self.pwm.set_pwm_freq(self.freq)

        self.motors_off() # Initialize motors to off

    def calculate_power(self, xAngle, yAngle):
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
        for channel in new_motor_power:
            self.req_pwr[channel] = ((new_motor_power[channel] + 1) / 4) + 1.5 # TODO Clean this up

    def set_motor(self, channel):
        if not 1.0 <= self.req_pwr[channel] <= 2.0: # Level should be between 1.0 and 2.0
            print("Error in set motor, trying to set motor", channel, "to", self.req_pwr[channel])
            return
        if sufficiently_different(self.curr_pwr[channel], self.req_pwr[channel]):
            self.pwm.set_pwm(self.channel[channel], 0, int(calcTicks(self.freq, self.req_pwr[channel])))
            self.curr_pwr[channel] = self.req_pwr[channel]

    def set_motors(self):
        for channel in 'ABCD':
            self.set_motor(channel)

    def motors_off(self):
        for channel in 'ABCD':
            self.req_pwr[channel] = 1.0
        self.set_motors()

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
