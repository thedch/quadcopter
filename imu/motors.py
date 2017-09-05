# Functions related to controlling the motors
# Author: Daniel Hunter
# Date: Sep 4 2017

import Adafruit_PCA9685

class MotorController:
    def __init__(self):
        self.channel = {
            'A': 0,
            'B': 3,
            'C': 2,
            'D': 1
        }

        self.current_motor_power = {
            'A': 1,
            'B': 1,
            'C': 1,
            'D': 1
        }

        self.pwm = Adafruit_PCA9685.PCA9685()
        self.freq = 50
        self.pwm.set_pwm_freq(self.freq)
        # TODO self.currentPower dict to pass into set_motors

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

        # Calculate absolute motor power based on relative
        for motor in new_motor_power:
            new_motor_power[motor] = ((new_motor_power[motor] + 1) / 4) + 1.5 # TODO Clean this up

        for m in 'A B C D':
            if sufficiently_different(current_motor_power[m], new_motor_power[m]):

    def set_motor(self, channel, level): # Level should be between 1.0 and 2.0
        self.pwm.set_pwm(self.channel[channel], 0, int(calcTicks(self.freq, level)))

    def set_motors(self, A=1, B=1, C=1, D=1): # TODO Pass in a dict instead?
        self.pwm.set_pwm(self.channel['A'], 0, int(calcTicks(self.freq, A)))
        self.pwm.set_pwm(self.channel['B'], 0, int(calcTicks(self.freq, B)))
        self.pwm.set_pwm(self.channel['C'], 0, int(calcTicks(self.freq, C)))
        self.pwm.set_pwm(self.channel['D'], 0, int(calcTicks(self.freq, D)))

    def kill_motors(self):
        self.set_motors() # Calling with no params defaults to off

def sufficiently_different(c, r): # current, requested
    if r > c * 1.02 or r < c * 0.98:
        return True
    return False


def calcTicks(hz, pulseInMilliseconds):
	cycle = 1000 / hz
	timePerTick = cycle / 4096
	ticks = pulseInMilliseconds / timePerTick
	return ticks
