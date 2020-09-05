# stringcar summary.py library 2017-12-30 v02

import board
import time
from digitalio import DigitalInOut, Direction, Pull
import adafruit_dotstar as dotstar

class Motor:
    """StringCar motor functions and attributes"""
    def __init__(self, pin_a1, pin_a2, mn, mx, r):
        self.min_speed = mn
        self.max_speed = mx
        self.acceleration_rate = r
        self.model = "RF550"
        self.vendor = "Nichibo"
        self.op_rpm = 1200
        self.op_voltage = 6
        self.op_current = 0.280
        self.min_voltage = 3
        self.max_voltage = 12
        self.shaft_diameter = 2.0  # mm

    def speed(self, vel=0):  # set motor speed, -100 to +100
        # ...
        return vel

    def accel(self, current=0, target=0, rate=0):  # current to target
        # ...
        return current

    def brake(self, hold=0.2, release=0.1):  # stop,freeze,then release
        # ...
        return 0

class Sensor:
    """return EOS sensor switch value, True/False"""
    def __init__(self, pin, s, t):
        self.eos_sensor = s
        self.cpu_temperature = t

    def eos_sensor(self, s):  # EOS sensor, True/False
        # ...
        return s

    def cpu_temperature(self, t):  # CPU temperature
        # ...
        return t

class Trimpot:
    """return potentiometer position, 0 to 100"""
    def __init__(self, pin, pos):
        self.position = pos
        self.minimum = 0
        self.maximum = 100

    def trimpot(self, pos):  # potentiometer position, 0 to 100
        # ...
        return pos

class Flash:
    """Flash integral dotstar, indexed colors"""
    def __init__(self, p):
        self.pin = p

    def flash(self, count=1, on=0.5, off=0.5, color=0):  # flash indexed colors
        # ...
        return True

class Beeper:
    """beep a tone using PWM pin connected piezo buzzer"""
    def __init__(self, pin, f, w):
        self.frequency = f
        self.wait = w

    def beep_on(self, f=440):  # start PWM piezo beeper
        # ...
        return True

    def beep_off(self, w=0):  # stop PWM piezo beeper after wait
        # ...
        return True

class Battery:
    """Battery attributes"""
    def __init__(self, cap, volt):
        self.capacity = cap
        self.voltage = volt

    def remain(self, r):  # calculate remaining capacity (minutes)
        # ...
        return r

class Pulley:
    """Pulley attributes"""
    def __init__(self, sd, cd, sh):
        self.shaft_diameter = sd
        self.core_diameter = cd
        self.shoulder_height = sh

# arduino-like map + constrain function from simpleio
def map_range(x, in_min, in_max, out_min, out_max):
    t = (x-in_min) * (out_max - out_min) / (in_max-in_min) + out_min
    if out_min <= out_max:
        return max(min(t, out_max), out_min)
    else:
        return min(max(t, out_max), out_min)
