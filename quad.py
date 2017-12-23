import time
from imu.imu import IMU
from motors.motors import MotorController

class Quadcopter:
  def __init__(self):
    self.sample_hz = 100
    self.motors = MotorController()
    self.imu = IMU(self.sample_hz)
    self.log_file = open("log.txt", "w")

    self.start_time = time.time()
    self.counter = 0

    self.log_variables = [self.counter, time.time() - self.start_time, self.imu.last_x, self.imu.last_y, self.imu.gyro_total_x, self.imu.gyro_total_y]
    self.header = ["count", "time", "lastX", "lastY", "gyroX", "gyroY"]

  def wait(self, start_time):
    '''Used to force a set Hz sampling rate instead of as fast as possible.'''
    time_diff = 1 / self.sample_hz
    while True:
        if (time.time() - start_time) >= (time_diff * self.counter):
            return

  def end_flight(self):
    self.motors.off()
    self.log_file.close()

  def format_row(self, row):
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

if __name__ == '__main__':
    print("This file is not designed to be run alone.")
