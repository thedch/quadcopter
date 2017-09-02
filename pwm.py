from __future__ import division
import Adafruit_PCA9685
from time import time, sleep

def calculateTicks(hz, pulseInMilliseconds):
	cycle = 1000 / hz
	timePerTick = cycle / 4096
	ticks = pulseInMilliseconds / timePerTick
	return ticks

def testTiming(duration):
    for i in range(0,4):
        ticks = calculateTicks(50, 1.7)
		# set_pwm(self, channel, on, off):
        pwm.set_pwm(i, 0, int(ticks))

    sleep(duration)

    for i in range(0,4):
        ticks = calculateTicks(50, 1.0)
        pwm.set_pwm(i, 0, int(ticks))

if __name__ == '__main__':
    pwm = Adafruit_PCA9685.PCA9685()
    pwm.set_pwm_freq(50)
    for i in range(0,4):
        ticks = calculateTicks(50, 1.0)
        pwm.set_pwm(i, 0, int(ticks))

    sleep(1)

    testTiming(1.1)

    while True:
        var = input("What pulse length in milliseconds would you like? ")
        ticks = calculateTicks(50, float(var))
        print(ticks)
        pwm.set_pwm(0, 0, int(ticks))
        pwm.set_pwm(1, 0, int(ticks))
        pwm.set_pwm(2, 0, int(ticks))
        pwm.set_pwm(3, 0, int(ticks))
