from __future__ import division
import Adafruit_PCA9685
import time


def calculateTicks(hz, pulseInMilliseconds):
	cycle = 1000 / hz
	timePerTick = cycle / 4096
	ticks = pulseInMilliseconds / timePerTick
	return ticks

if __name__ == '__main__':
    max = calculateTicks(50, 2)
    min = calculateTicks(50, 1)
    print max
    print min

    pwm = Adafruit_PCA9685.PCA9685()
    pwm.set_pwm_freq(50)

    while True:
        var = raw_input("What pulse length in milliseconds would you like? ")
        ticks = calculateTicks(50, float(var))
        print ticks
        pwm.set_pwm(0, 0, int(ticks))
