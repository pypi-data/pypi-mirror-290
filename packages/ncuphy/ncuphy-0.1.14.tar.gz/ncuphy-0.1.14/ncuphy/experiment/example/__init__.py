__list__ = sorted(['StepperMotor', "ADS1115", "MPU9250", "MPU6050"])

__which__ = input(f"Which module do you want to import? \n{__list__}\nEnter the module name: ")

assert __which__ in __list__, f"Module {__which__} not found in {__list__}"


__stepper_motor_example = """
from ncuphy.experiment import StepperMotor
import time

# display log, not necessary ---------------------------------------------

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# -----------------------------------------------------------------------------

# define the pins
pul = 26
dir = 19
ena = 13

# define the delay between pulses
pulse_delay = 0.001

# create the stepper motor object
motor = StepperMotor(pul, dir, ena, pulse_delay)



# move the stepper motor by 1000 steps
motor.step(1000)
time.sleep(2)



# move the stepper motor in the other direction by 1500 steps
motor.step(-1800)
time.sleep(2)



# move the stepper motor to the home position
motor.home()
time.sleep(2)



# move the stepper motor again by 100 steps
motor.step(1200)
time.sleep(2)



# get the current position
position = motor.position
print(f"Current position: {position}")



# set the current position as the home position
motor.sethome()
"""


if __which__ == "StepperMotor":
    with open('Example_StepperMotor.py', 'w') as f:
        f.write(__stepper_motor_example)
else:
    print("Example not found.")