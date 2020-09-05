# boomerpong gen_2 2018-03-25 v24.py
# experimental version to test stringcar library motor control scheme
# library: stringcar 2018-03-24 v07.py
print("boomerpong gen_2 2018-03-25 v24.py")

import time
import stringcar as sc

#   ### MOTOR SPECIFICATIONS ###
# motor characteristics for BoomerPong 3v2 6v 2100RPM motor
stop_motor_volt = 2.0
min_motor_volt = 5.0
max_motor_volt = 9.0
power_volt = 9.0  # battery monitoring could change this parameter
accel_rate = 0.5  # stop to max speed accel/decel (sec)
# rated_motor_volt = 6.0
# rated_motor_rpm = 2100
# effective_pulley_dia_inch = 0.0

motor_specs = stop_motor_volt, min_motor_volt, max_motor_volt, power_volt, accel_rate

#   ### VARIABLES ###
speed = 0       # -1.0 (rev) to +1.0 (fwd)
lap = -1
dist = 0        # (sec)

# ### SETTINGS and SETUP ####

# play hello tune
sc.hello()

# send motor specifications to stringcar library
# wait to start, then receive min speed, accel rate, and mode values
min_speed, mode, motor_params = sc.setup(motor_specs)
print("BATTERY VOLTAGE = ", sc.trimpot(), "  : CPU TEMPERATURE = ", sc.cpu_temp(), "F")
print("MINIMUM SPEED = ", min_speed, " : MODE = ", mode)
print("MOTOR VOLTS SPECIFICATIONS (stop, min, max, power source, accel_rate) = ", motor_specs)
print("MOTOR DUTY_CYCLE PARAMETERS (zero, min, max) = ", motor_params)

sc.time.sleep(1)  # allow time to remove hand from car

# set initial direction to reverse; it'll get flipped later
direction = -1
sc.busy.value = False

# #### MAIN LOOP #####
while True:
    # RUSH test
    if sc.trimpot() < 3.0:
        sc.rush()

    lap = lap + 1

    # Boomerang stop at end of lap 1
    if not mode and lap > 1:
        speed = sc.accel(speed, 0, 0, motor_params) # release the brakes
        print("end of Boomerang lap")
        while True:
            sc.beep_on(494)
            sc.flash(7, 1, .01, 3)
            sc.beep_off(.5)
            print(".")

    t0 = time.monotonic()
    dist = 0

    direction = direction * -1  # flip motor direction
    if lap == 0:
        speed = sc.accel(speed, min_speed * direction, accel_rate, motor_params)
        at_min_speed_flag = True
    else:
        speed = sc.accel(speed, 1.0 * direction, accel_rate, motor_params)
        at_min_speed_flag = False

    # escape EOS
    while not sc.sensor_eos.value:
        sc.busy.value = True
        dist = time.monotonic() - t0

        # 1+ laps and at slowing dist and at maximum speed
        if lap > 0 and dist > (str_len) and not at_min_speed_flag:
            at_min_speed_flag = True
            speed = sc.accel(speed, min_speed * direction, accel_rate, motor_params)
    sc.busy.value = False

    # normal travel; wait for EOS
    while sc.sensor_eos.value:
        dist = time.monotonic() - t0

        # 1+ laps and at slowing dist and at maximum speed
        if lap > 0 and dist > str_len and not at_min_speed_flag:
            at_min_speed_flag = True
            speed = sc.accel(speed, min_speed * direction, accel_rate, motor_params)

    # insert LOST test here
    speed = sc.speed(0, motor_params) # put on the brakes
    sc.busy.value = True
    sc.beep_on(656)  # E5
    sc.time.sleep(0.5)
    sc.beep_off()

    # string length calculation
    if lap == 0:
        # calibration lap; scale string length to max speed based on min speed
        #   dist-(accel_rate/2) is adjusted distance with initial accel to min speed
        str_len = (dist - (accel_rate / 2)) * min_speed
        print("CALIBRATE lap =", lap, " : dist = ", dist, " : str_len = ", str_len, " : min speed = ", min_speed)
    else:
        # calculate new string length
        if dist > str_len:
            # adjust distance if longer than previous string length
            #   str_len is initial distance including initial accel to max speed
            #   ((dist-str_len)*min_speed) is raw dist measured after str_len is reached
            #   ((accel_rate/2)*(1.0-min_speed)) is slowing distance from full to min speed
            dist = str_len + ((dist - str_len) * min_speed) + ((accel_rate / 2) * (1.0 - min_speed))

        # use moving average to approximate the new string length
        #   (also known as successive approximation)
        str_len = (str_len + ((dist - str_len)/2))
        print("lap =", lap, " : dist = ", dist, " : NEW str_len =", str_len)

    # return to top of the main loop
