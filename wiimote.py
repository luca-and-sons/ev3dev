from ev3dev.auto import *
import time
import cwiid

def clamp(value, lower, upper):
    return min(upper, max(value, lower))


print('press 1+2 on the wiimote now')
time.sleep(1)
w = cwiid.Wiimote()
print('connected?')
w.led = 6
w.rpt_mode = cwiid.RPT_ACC | cwiid.RPT_BTN


left_motor = Motor(OUTPUT_B)
left_motor.reset()
left_motor.run_mode = 'forever'
left_motor.regulation_mode = 'on'

right_motor = Motor(OUTPUT_C)
right_motor.reset()
right_motor.run_mode = 'forever'
right_motor.regulation_mode = 'on'

arm = Motor(OUTPUT_D)
arm.reset()
arm.run_mode = 'forever'
arm.regulation_mode = 'off'

target_distance = 8
top_speed = 720

left_motor.run = 1
right_motor.run = 1

last_btn_state = 0
move = 0

try:
    while True:
        state = w.state

        buttons = state['buttons']
        if buttons != last_btn_state:
            if buttons & cwiid.BTN_MINUS:
                top_speed -= 10
                print(top_speed)
            if buttons & cwiid.BTN_PLUS:
                top_speed += 10
                print(top_speed)
            if buttons & cwiid.BTN_2:
                move = 1
            elif buttons & cwiid.BTN_1:
                move = -1
            else:
                move = 0
            if buttons & cwiid.BTN_LEFT:
                arm.duty_cycle_sp = 100
                arm.run = 1
            elif buttons & cwiid.BTN_RIGHT:
                arm.duty_cycle_sp = -100
                arm.run = 1
            else:
                arm.run = 0
            print(top_speed, move)
            last_btn_state = buttons

        if move:
            acc = state['acc']
            tilt = (clamp(acc[1], 95, 145) - 120) / 25.0  # roughly between -0.5 and 0.5
            turn = top_speed * tilt
            turn = clamp(turn, -abs(top_speed), abs(top_speed))
            left_motor.pulses_per_second_sp = int(top_speed - turn) * move
            right_motor.pulses_per_second_sp = int(top_speed + turn) * move
        else:
            left_motor.pulses_per_second_sp = 0
            right_motor.pulses_per_second_sp = 0
finally:
    left_motor.run = 0
    right_motor.run = 0
