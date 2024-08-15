import time
import logging
import RPi.GPIO as GPIO


def sleep(t):
    start = time.perf_counter()
    while time.perf_counter() - start < t:
        pass
    

class StepperMotor:
    """
    Represents a stepper motor.

    Args:
        pul (int): The GPIO pin number for the PUL (pulse) signal.
        dir (int): The GPIO pin number for the DIR (direction) signal.
        ena (int): The GPIO pin number for the ENA (enable) signal.
        step_delay (float or int): The delay between steps in seconds.

    Attributes:
        pul (int): The GPIO pin number for the PUL (pulse) signal.
        dir (int): The GPIO pin number for the DIR (direction) signal.
        ena (int): The GPIO pin number for the ENA (enable) signal.
        step_delay (float or int): The delay between steps in seconds.
        position (int): The current position of the stepper motor.

    Methods:
        step(steps: int): Moves the stepper motor by the specified number of steps.
        
        sethome(): Sets the current position as the home position.
        home(): Moves the stepper motor to the home position.
        
        hold(): Holds the stepper motor in its current position.
        release(): Releases the stepper motor.
    """
    def __init__(self, pul, dir, ena, step_delay):
        """
        Initializes a StepperMotor instance.

        Args:
            pul (int): The GPIO pin number for the PUL (pulse) signal.
            dir (int): The GPIO pin number for the DIR (direction) signal.
            ena (int): The GPIO pin number for the ENA (enable) signal.
            step_delay (float or int): The delay between steps in seconds.
        """
        gpiomode = GPIO.getmode()
        
        if gpiomode is None:
            GPIO.setmode(GPIO.BCM)
            
        logging.info(f"GPIO mode: {GPIO.getmode()}")
        logging.info(f"Step Delay: {step_delay} s")
        
        assert type(pul) == int
        assert type(dir) == int
        assert type(ena) == int
        assert type(step_delay) in [float, int]
        
        self.pul = pul
        self.dir = dir
        self.ena = ena
        self.step_delay = step_delay
        
        GPIO.setup(self.pul, GPIO.OUT)
        GPIO.setup(self.dir, GPIO.OUT)
        GPIO.setup(self.ena, GPIO.OUT)
        
        self._position = 0


    def _pulse(self):
        """
        Sends a pulse signal to the stepper motor driver.
        """
        GPIO.output(self.pul, GPIO.HIGH)
        sleep(self.step_delay/2)
        GPIO.output(self.pul, GPIO.LOW)
        sleep(self.step_delay/2)
        
        
    @property
    def position(self):
        """
        int: The current position of the stepper motor.
        """
        return self._position
    
    
    def sethome(self):
        """
        Sets the current position as the home position.
        """
        self._position = 0
        logging.info(f"Home position set. Current position: {self._position}")
        
        
    def home(self):
        """
        Moves the stepper motor to the home position.
        """
        self.step(-self.position)
        logging.info("Homed.")
        self.sethome()
        
        
    def step(self, steps):
        """
        Moves the stepper motor by the specified number of steps.

        Args:
            steps (int): The number of steps to move the stepper motor.
        """
        assert type(steps) == int
        
        GPIO.output(self.dir, GPIO.HIGH if steps > 0 else GPIO.LOW)
        GPIO.output(self.ena, GPIO.LOW)
        
        sleep(self.step_delay)
        
        for _ in range(abs(steps)):
            self._pulse()
            self._position += 1 if steps > 0 else -1

        
        GPIO.output(self.ena, GPIO.HIGH)
        logging.info(f"Moved {steps} steps. Current position: {self._position}")
        
        
    def hold(self):
        """
        Holds the stepper motor in its current position.
        """
        GPIO.output(self.ena, GPIO.LOW)
        sleep(self.step_delay)
        logging.info("Holding.")
        
        
    def release(self):
        """
        Releases the stepper motor.
        """
        GPIO.output(self.ena, GPIO.HIGH)
        sleep(self.step_delay)
        logging.info("Released.")
        
        
    def __del__(self):
        GPIO.cleanup()
        logging.info("GPIO cleaned up.")