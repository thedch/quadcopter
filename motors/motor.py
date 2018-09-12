import Adafruit_PCA9685
from time import sleep

class Motor:
    def __init__(self, channel):
        self.channel = channel
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.freq = 50
        self.pwm.set_pwm_freq(self.freq)

    def set_power(self, power):
        assert 1 <= power <= 2
        self.pwm.set_pwm(self.channel, 0, int(calc_ticks(self.freq, power)))

def calc_ticks(hz, pulseInMilliseconds):
    cycle = 1000 / hz
    timePerTick = cycle / 4096
    ticks = pulseInMilliseconds / timePerTick
    return ticks

if __name__ == '__main__':
    motors = [Motor(0), Motor(1), Motor(2), Motor(3)]
    for motor in motors: motor.set_power(1)
    sleep(2)
    for motor in motors: motor.set_power(2)
    sleep(2)
    for motor in motors: motor.set_power(1)

