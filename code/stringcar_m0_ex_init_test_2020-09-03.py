# stringcar_m0_ex_init_test_2020-09-03
# Cedar Grove StringCar M0 Express v06 initial test
import board
import time
import pulseio
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn
import adafruit_dotstar as dotstar
from simpleio import map_range, tone

# Red Status LED
led = DigitalInOut(board.LED_STATUS)
led.direction = Direction.OUTPUT
led.value = False

# The RGB LED
dot = dotstar.DotStar(board.DOTSTAR_CI, board.DOTSTAR_DI, 1, brightness=0.1)
dot[0] = (128, 0, 128)  # yellow startup status

import busio

try:
    stemma = busio.I2C(board.SCL, board.SDA)
    stemma_connected = True
    print("STEMMA DEVICE CONNECTED")
except:
    stemma_connected = False
    print("Stemma device disconnected")
    time.sleep(3)

# Analog input on VOLTAGE_MONITOR
v_plus = AnalogIn(board.VOLTAGE_MONITOR)

# Motor controller outputs
motor_out_1 = DigitalInOut(board.MOTOR_OUT_1)
motor_out_1.direction = Direction.OUTPUT
motor_out_2 = DigitalInOut(board.MOTOR_OUT_2)
motor_out_2.direction = Direction.OUTPUT

# Piezo speaker outputs
piezo = board.PIEZO
tone(piezo, 880, duration=0.3)  # A5

# Sensor input with pullup on SENSOR_IN
sensor = DigitalInOut(board.SENSOR_IN)
sensor.direction = Direction.INPUT
sensor.pull = Pull.UP


######################### HELPERS ##############################

# Helper to convert analog input to voltage
def getVoltage(pin):
    return 2 * (pin.value * 3.3) / 65536

# Helper to give us a nice color swirl
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if (pos < 0) or (pos > 255):
        return (0, 0, 0)
    if pos < 85:
        return (int(255 - pos*3), int(pos*3), 0)
    elif pos < 170:
        pos -= 85
        return (0, int(255 - (pos*3)), int(pos*3))
    else:
        pos -= 170
        return (int(pos*3), 0, int(255 - pos*3))

######################### MAIN LOOP ##############################


i = 0
while True:
  led.value = True
  motor_out_1.value = True
  motor_out_2.value = False

  # spin internal LED around! autoshow is on
  dot[0] = wheel(i & 255)

  if sensor.value: sens = 3.3
  else: sens = 0

  # Read analog voltage on VOLTAGE_MONITOR
  print((i & 255))
  print('i: %3.0f  wheel: %6x' % (i, i & 255), wheel(i & 255))
  print("V+ : %0.2f" % (2 * getVoltage(v_plus)))
  print( (getVoltage(v_plus), sens))

  if not sensor.value:
      print("Sensor closed to ground!")

  i = (i+1) % 256  # run from 0 to 255

  led.value = False
  motor_out_1.value = False
  motor_out_2.value = True

  time.sleep(0.05) # make bigger to slow down
