# Functions related to controlling the motors
# Author: Daniel Hunter
# Date: Sep 4 2017

import Adafruit_PCA9685

class MotorController
    def __init__(self):
        self.channel = {
            'A' = 0,
            'B' = 3,
            'C' = 2,
            'D' = 1
        }

        self.pwm = Adafruit_PCA9685.PCA9685()
        self.freq = 50
        self.pwm.set_pwm_freq(self.freq)
        # TODO self.currentPower dict to pass into set_motors

        self.set_motors() # Init motors to off

    def calculatePower(xAngle, yAngle):
        # Calculate relative desired motor power based on angle imbalance
        # Scale values to be -1 to 1
        xAngle = max(min(xAngle / 10, 1), -1)
        yAngle = max(min(yAngle / 10, 1), -1)

        # Set motor values based on average axis tilt
        motors = {
            'A' = (yAngle - xAngle) / 2
            'B' = (yAngle + xAngle) / 2
            'C' = motors['A'] * (-1)
            'D' = motors['B'] * (-1)
        }

        # Calculate absolute motor power based on relative
        for motor in motors:
            motors[motor] = ((motors[motor] + 1) / 4) + 1.5 # TODO Clean this up

        return motors

    def set_motors(self, A=1, B=1, C=1, D=1): # TOD Pass in a dict instead?
        pwm.set_pwm(channel['A'], 0, int(calcTicks(self.freq, A)))
        pwm.set_pwm(channel['B'], 0, int(calcTicks(self.freq, B)))
        pwm.set_pwm(channel['C'], 0, int(calcTicks(self.freq, C)))
        pwm.set_pwm(channel['D'], 0, int(calcTicks(self.freq, D)))

    def kill_motors(self):
        self.set_motors() # Calling with no params defaults to off

def calcTicks(hz, pulseInMilliseconds):
	cycle = 1000 / hz
	timePerTick = cycle / 4096
	ticks = pulseInMilliseconds / timePerTick
	return ticks
