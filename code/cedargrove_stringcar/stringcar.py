# stringcar 2020-09-06 v08.py
# test of new motor control scheme

import board
from microcontroller import cpu
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn
from simpleio import map_range
import adafruit_dotstar as dotstar
import time
import pulseio

print("stringcar 2020-09-05 v08.py")

# set up dotstar indicator output (GBR orientation)
dot = dotstar.DotStar(board.DOTSTAR_CI, board.DOTSTAR_DI, 1, brightness=0.5)

# set up busy indicator output (red LED)
busy = DigitalInOut(board.LED_STATUS)
busy.direction = Direction.OUTPUT

# set up motor controller outputs
ain01 = pulseio.PWMOut(board.MOTOR_OUT_1, frequency=45, duty_cycle=0)
ain02 = pulseio.PWMOut(board.MOTOR_OUT_2, frequency=45, duty_cycle=0)

# set up EOS sensor switch input
sensor_eos = DigitalInOut(board.SENSOR_IN)
sensor_eos.direction = Direction.INPUT
sensor_eos.pull = Pull.UP

# Analog input on VOLTAGE_MONITOR
v_plus = AnalogIn(board.VOLTAGE_MONITOR)

# set up potentiometer control input
#ctl = AnalogIn(board.D1)

# set up piezo output
piezo = pulseio.PWMOut(board.PIEZO, duty_cycle=0, frequency=440, variable_frequency=True)

def setup(motor_specs):
    busy.value = True
    # receive default motor characteristics from main code
    stop_motor_volt, min_motor_volt, max_motor_volt, power_volt, accel_rate = motor_specs

    # motor parameter calculations (motor_params)
    mode = False  # Boomerang mode default
    stop_duty_cycle = map_range(stop_motor_volt, 0, power_volt, 0, 1.0)
    min_duty_cycle = map_range(min_motor_volt, 0, power_volt, 0, 1.0)
    max_duty_cycle = map_range(max_motor_volt, 0, power_volt, 0, 1.0)

    # minimum motor speed calculation
    min_speed = map_range(min_motor_volt, stop_motor_volt, max_motor_volt, 0, 1.0)

    # test for Pong (default) versus Boomerang mode
    if not sensor_eos.value:
        mode = False    # Boomerang mode
        print("Boomerang Mode")
    else:
        mode = True     # Pong mode
        print("Pong Mode")

    while not sensor_eos.value:
        flash(0, 1, 0.01, 0.2)
    while sensor_eos.value:
        if mode:
            flash(5, 1, 0.01, 0.2)
        else:
            flash(6, 1, 0.02, 0.4)
    motor_params = stop_duty_cycle, min_duty_cycle, max_duty_cycle
    busy.value = False
    return min_speed, mode, motor_params

def speed(vel, motor_params):  # set motor speed, -1.0 to +1.0
    busy.value = True
    stop_duty_cycle, min_duty_cycle, max_duty_cycle = motor_params
    if vel > 0:  # forward
        ain01.duty_cycle = int(map_range(abs(vel), 0, 1.0, stop_duty_cycle, max_duty_cycle) * 0xFFFF)
        ain02.duty_cycle = 0x0000
        dot[0] = [int(abs(vel)*150), 0, 0]
        #print('forward')
    if vel < 0:  # reverse
        ain01.duty_cycle = 0x0000
        ain02.duty_cycle = int(map_range(abs(vel), 0, 1.0, stop_duty_cycle, max_duty_cycle) * 0xFFFF)
        dot[0] = [0, 0, int(abs(vel)*150)]
        #print('reverse')
    if vel == None:  # coast
        ain01.duty_cycle = 0x0000
        ain02.duty_cycle = 0x0000
        dot[0] = [75, 0, 64]  # COAST: pale yellow
    if vel == 0:  # brake
        ain01.duty_cycle = 0xFFFF  # 65,535 (16-bits)
        ain02.duty_cycle = 0xFFFF  # 65,535 (16-bits)
        dot[0] = [102, 0, 90]  # BRAKE: yellow
    busy.value = False
    return vel

def accel(current, target, accel_rate, motor_params):  # current to target
    busy.value = True
    stop_duty_cycle, min_duty_cycle, max_duty_cycle = motor_params
    while current > target:
        current = current - 0.01
        if current < -1.0: current = -1.0
        speed(current, motor_params)
        time.sleep(accel_rate / 100)
    while current < target:
        current = current + 0.01
        if current > 1.0: current = 1.0
        speed(current, motor_params)
        time.sleep(accel_rate / 100)
    speed(current, motor_params)
    busy.value = False
    return current

def cpu_temp():  # CPU temperature in F
    return (cpu.temperature * 9/5)+32

# Helper to convert analog input to voltage
def get_batt():
    return 2 * (v_plus.value * 3.3) / 65536

def flash(color=0, count=1, on=0.5, off=0.5):  # blink indexed colors
    #print('flash: blink indexed colors')
    busy.value = True
    for i in range(count):
        if color == 0:
            dot[0] = [153, 153, 153]  # flash white
        if color == 5:
            dot[0] = [0, 153, 153]  # PONG MODE: violet
        if color == 6:
            dot[0] = [0, 255, 0]  # BOOMERANG MODE: blue
        if color == 7:
            dot[0] = [0, 153, 0]  # END OF BOOM: pale blue
        beep_on(784)  # E5
        beep_off(on)
        dot[0] = [0, 0, 0]  # off
        time.sleep(off)
    busy.value = False
    return

def beep_on(f=440):  # start PWM piezo beeper
    piezo.frequency = f
    piezo.duty_cycle = int(65535/2)  # tone on, 50%
    return

def beep_off(w=0):  # stop PWM piezo beeper after wait
    if w != 0:
        time.sleep(w)
    piezo.duty_cycle = 0  # tone off
    return

def hello():  # play hello tune
    busy.value = True
    dot[0] = [200, 100, 0]  # teal
    beep_on(523 * 1)  # C5
    beep_off(0.25)
    beep_on(784 * 1)  # G5
    beep_off(0.25)
    beep_on(659 * 1)  # E5
    beep_off(1)
    time.sleep(0.25)
    dot[0] = [0, 0, 0]  # dark
    busy.value = False
    return

def lost(str_len):  # Lost On Stretched Twine
    print("LOST: Lost On Stretched Twine : string length = ", str_len)
    return

def rush(str_len=0):  # Return Unharmed to String Home
    print("RUSH: Return Unharmed to String Home : string length = ", str_len)
    return
