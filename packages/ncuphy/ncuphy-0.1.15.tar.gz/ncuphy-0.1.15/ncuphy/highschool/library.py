import numpy as np
import time
import logging
import ncuphy.highschool.ncugrovepi as ncugrovepi


class AnalogPort:
    def __init__(self, pin: int) -> None:
        self.__available_ports = [0, 1, 2]
        self.__bits = 10
        self.__ref_voltage = 5

        assert pin in self.__available_ports

        self.pin = pin

        ncugrovepi.pinMode(self.pin, "INPUT")

    def __raw(self) -> int:
        while True:
            try:
                value = ncugrovepi.analogRead(self.pin)
                assert value <= 2 ** self.__bits
                return value
            except:
                logging.warning("Analog read raw directly from adc failed. Retrying...")
                continue

    @property
    def value(self) -> int:
        return self.__raw()

    @property
    def voltage(self) -> float:
        return self.__raw() * self.__ref_voltage / 2 ** self.__bits

    def sample(self, N: int, mode='voltage') -> tuple[float, float]:
        assert mode in ['voltage', 'value']
        assert isinstance(N, int)
        assert N > 0

        data = np.empty(N)

        if mode == 'voltage':
            for i in range(N):
                data[i] = self.voltage
        elif mode == 'value':
            for i in range(N):
                data[i] = self.value

        return np.mean(data), np.std(data)


class DigitalPort:
    def __init__(self, pin: int, mode: str) -> None:
        self.__available_ports = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        self.__modes = ['OUTPUT', 'INPUT']

        assert pin in self.__available_ports
        assert mode in self.__modes

        self.pin = pin

        ncugrovepi.pinMode(self.pin, mode)

    def __write(self, value: int) -> None:
        assert value in [0, 1]
        ncugrovepi.digitalWrite(self.pin, value)

    def high(self) -> None:
        self.__write(1)

    def low(self) -> None:
        self.__write(0)

    def pulse(self, duration: float) -> None:
        assert isinstance(duration, (int, float))
        assert duration > 0

        ncugrovepi.digitalWrite(self.pin, 1)
        start = time.time()

        while time.time() - start < duration:
                pass

        ncugrovepi.digitalWrite(self.pin, 0)
        start = time.time()

        while time.time() - start < duration:
                pass


class StepperMotor:
    def __init__(self, port: int) -> None:
        GND = "GND"
        VCC = "VCC"
        DIR = "DIR"
        PUL = "PUL"

        self.__available_ports = [0, 2, 3, 4, 5, 6, 7, 8]

        self.__port_mapping = {0: (GND, VCC, 15, 14),
                               2: (GND, VCC, 3, 2),
                               3: (GND, VCC, 4, 3),
                               4: (GND, VCC, 5, 4),
                               5: (GND, VCC, 6, 5),
                               6: (GND, VCC, 7, 6),
                               7: (GND, VCC, 8, 7),
                               8: (GND, VCC, 9, 8)}

        self.__default_port_config = (GND, VCC, DIR, PUL)

        assert port in self.__available_ports

        self.port = port
        self.gnd, self.vcc, self.dir, self.pul = self.__port_mapping[port]

        self.dir_port = DigitalPort(self.dir, "OUTPUT")
        self.pul_port = DigitalPort(self.pul, "OUTPUT")

    def step(self, steps: int) -> None:
        assert isinstance(steps, int)

        delay = 0.00075

        if steps < 0:
            self.dir_port.high()
        else:
            self.dir_port.low()

        for i in range(abs(steps)):
            start = time.time()

            self.pul_port.high()
            while time.time() - start < delay:
                pass

            start = time.time()

            self.pul_port.low()
            while time.time() - start < delay:
                pass

    def move(self, microsteps, displacement):
        assert isinstance(microsteps, int)
        assert isinstance(displacement, (int, float))

        steps = int(microsteps * displacement / 1.25)
        self.step(steps)


class OPT101:
    def __init__(self, port: int):
        GND = "GND"
        VCC = "VCC"
        ADC = "ADC"
        EMPTY = "EMPTY"

        self.__available_ports = [0, 1, 2]

        self.__port_mapping = {0: (GND, VCC, 1, 0),
                               1: (GND, VCC, 2, 1),
                               2: (GND, VCC, 3, 2)}

        self.__default_port_config = (GND, VCC, ADC, EMPTY)

        assert port in self.__available_ports

        self.port = port

        self.gnd, self.vcc, self.adc, self.empty = self.__port_mapping[port]
        self.adc_port = AnalogPort(self.adc)

    @property
    def voltage(self):
        return self.adc_port.voltage

    @property
    def value(self):
        return self.adc_port.value

    def sample(self, N: int, mode='voltage') -> tuple[float, float]:
        assert mode in ['voltage', 'value']
        assert isinstance(N, int)
        assert N > 0

        return self.adc_port.sample(N, mode)


class PlanksConstant:
    def __init__(self, port: int):
        GND = "GND"
        VCC = "VCC"
        CH1 = "CH1"
        CH2 = "CH2"
        
        self.__available_ports = [0, 1, 2]
        
        self.__port_mapping = {0: (GND, VCC, 0, 1),
                                 1: (GND, VCC, 2, 1),
                                 2: (GND, VCC, 3, 1)}
        
        self.__default_port_config = (GND, VCC, CH1, CH2)
        
        assert port in self.__available_ports
        
        self.port = port
        
        self.gnd, self.vcc, self.ch1, self.ch2 = self.__port_mapping[port]
        self.ch1_port = AnalogPort(self.ch1)
        self.ch2_port = AnalogPort(self.ch2)
        
    @property
    def voltage(self):
        return self.ch1_port.voltage, self.ch2_port.voltage
    
    @property
    def value(self):
        return self.ch1_port.value, self.ch2_port.value
    
    def sample(self, N: int, mode='voltage') -> tuple[float, float]:
        assert mode in ['voltage', 'value']
        assert isinstance(N, int)
        assert N > 0
        
        return self.ch1_port.sample(N, mode), self.ch2_port.sample(N, mode)

def array(item):
    return item if isinstance(item, np.ndarray) else np.array(item)
