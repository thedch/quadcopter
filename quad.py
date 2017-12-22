import time
from imu.imu import IMU
from motors.motors import MotorController

class Quadcopter:
  def __init__(self):
    self.motors = MotorController()
    self.imu = IMU()

    self.log_variables = [counter, time.time() - start_time, rot_x, rot_y, last_x, last_y, gyro_x_delta, gyro_y_delta, self.motors.req_pwr['A'], self.motors.req_pwr['B'], self.motors.req_pwr['C'], self.motors.req_pwr['D']]
    self.header = ["count", "time", "rotX", "rotY", "lastX", "lastY", "gyroX", "gyroY", "motA", "motB", "motC", "motD"]

    self.sample_hz = 100
    self.K = 0.98

  def initialReadings(self):

  def wait(count, start_time):
    '''Used to force a set Hz sampling rate instead of as fast as possible.'''
    time_diff = 1 / self.sample_hz
    while True:
        if (time.time() - start_time) >= (time_diff * count):
            return

  def format_row(row):
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

