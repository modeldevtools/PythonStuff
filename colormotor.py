#!/usr/bin/env python3
# An EV3 Python (library v2) solution to Exercise 3
# of the official Lego Robot Educator lessons that
# are part of the EV3 education software
import ev3dev2
from ev3dev2.motor import MoveTank, OUTPUT_B, OUTPUT_C
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.button import Button
from time import sleep

btn = Button() # we will use any button to stop script
tank_pair = MoveTank(OUTPUT_B, OUTPUT_C)
myMotor = ev3dev2.motor.Motor(OUTPUT_B)
# Connect an EV3 color sensor to any sensor port.
cl = ColorSensor()

while not btn.any():    # exit loop when any button pressed
    # if we are over the black line (weak reflection)
    if cl.reflected_light_intensity<30:
        # medium turn right
        tank_pair.on(left_speed=0, right_speed=-50)
        print(myMotor.speed)

    else:   # strong reflection (>=30) so over white surface
        # medium turn left
        tank_pair.on(left_speed=-50, right_speed=0)
        print(myMotor.speed)

    sleep(0.1) # wait for 0.1 seconds
tank_pair.on(left_speed=0, right_speed=0)
