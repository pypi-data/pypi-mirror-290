from smbus2 import SMBus
import time
import math
from ..mpu6050 import MPU6050
import numpy as np

class AK8963:
    """
    This class represents the AK8963 magnetometer and provides methods to initialize and read magnetometer data.

    Args:
        address (int): I2C address of the AK8963 sensor (default is 0x0C).
        mode (int): Measurement mode (default is 0x16 for continuous measurement mode 2 with 16-bit output).

    Raises:
        AssertionError: If any of the input arguments are invalid.

    Methods:
        get_mag_data(): Get the magnetometer data in microteslas.
        calculate_heading(x, y): Calculate the heading (direction) based on X and Y magnetometer data.
        
    Attributes:
        WHO_AM_I (int): Device ID register address.
        
        ST1 (int): Status register address.
        HXL (int): X-axis data low byte register address.
        HXH (int): X-axis data high byte register address.
        HYL (int): Y-axis data low byte register address.
        HYH (int): Y-axis data high byte register address.
        HZL (int): Z-axis data low byte register address.
        HZH (int): Z-axis data high byte register address.
        
        ST2 (int): Status 2 register address.
        
        CNTL1 (int): Control register 1 address.
        CNTL2 (int): Control register 2 address.
        
        ASAX (int): Sensitivity adjustment value register address for X-axis.
        ASAY (int): Sensitivity adjustment value register address for Y-axis.
        ASAZ (int): Sensitivity adjustment value register address for Z-axis.
    """

    # Register Addresses
    WHO_AM_I = 0x00
    ST1 = 0x02
    HXL = 0x03
    HXH = 0x04
    HYL = 0x05
    HYH = 0x06
    HZL = 0x07
    HZH = 0x08
    ST2 = 0x09
    CNTL1 = 0x0A
    CNTL2 = 0x0B
    ASAX = 0x10
    ASAY = 0x11
    ASAZ = 0x12

    def __init__(self, address=0x0C, mode=0x16):
        self.address = address
        self.mode = mode
        self.bus = SMBus(1)

        # Initialize the sensor
        self.mag_adj = self.initialize_sensor()

    def initialize_sensor(self):
        """
        Initialize the AK8963 sensor by setting it to Fuse ROM access mode and reading sensitivity adjustment values.

        Returns:
            list: Sensitivity adjustment factors for the X, Y, and Z axes.
        """
        # Reset the sensor
        self.bus.write_byte_data(self.address, AK8963.CNTL2, 0x01)
        time.sleep(0.1)

        # Enter Fuse ROM access mode
        self.bus.write_byte_data(self.address, AK8963.CNTL1, 0x0F)
        time.sleep(0.01)

        # Read sensitivity adjustment values
        mag_adj = [
            (self.bus.read_byte_data(self.address, AK8963.ASAX) - 128) / 256.0 + 1.0,
            (self.bus.read_byte_data(self.address, AK8963.ASAY) - 128) / 256.0 + 1.0,
            (self.bus.read_byte_data(self.address, AK8963.ASAZ) - 128) / 256.0 + 1.0
        ]

        # Set to continuous measurement mode with 16-bit output
        self.bus.write_byte_data(self.address, AK8963.CNTL1, self.mode)
        time.sleep(0.01)

        return mag_adj

    def _read_raw_data(self, addr):
        """
        Read raw magnetometer data from the specified register address.

        Args:
            addr (int): The register address to read data from.

        Returns:
            int: The raw magnetometer data as a signed 16-bit integer.
        """
        low = self.bus.read_byte_data(self.address, addr)
        high = self.bus.read_byte_data(self.address, addr + 1)
        value = (high << 8) | low
        
        # Convert to signed value
        if value > int(2 ** 15):
            value -= 2 ** 16
        return int(value)

    def get_mag_data(self):
        """
        Get the magnetometer data from the AK8963 sensor in microteslas (μT).

        Returns:
            dict: A dictionary containing the magnetometer data with keys 'x', 'y', and 'z'.
        """
        if self.bus.read_byte_data(self.address, AK8963.ST1) & 0x01:
            x = self._read_raw_data(AK8963.HXL) * self.mag_adj[0]
            y = self._read_raw_data(AK8963.HYL) * self.mag_adj[1]
            z = self._read_raw_data(AK8963.HZL) * self.mag_adj[2]

            # Ensure data is not saturated
            if self.bus.read_byte_data(self.address, AK8963.ST2) & 0x08 == 0:
                return {'x': x, 'y': y, 'z': z}

        return None

    def calculate_heading(self, x, y):
        """
        Calculate the heading (direction) based on magnetometer data.

        Args:
            x (float): X-axis magnetometer data.
            y (float): Y-axis magnetometer data.

        Returns:
            float: Heading angle in degrees relative to magnetic north.
        """
        heading = math.atan2(y, x) * (180 / math.pi)
        if heading < 0:
            heading += 360
        return heading


class MPU9250:
    def __init__(self, acc_address=0x68, accel_fsr=2, gyro_fsr=250, sample_rate_divider=1, digital_lowpass_level=0, ext_sync_set=0, mag_address = 0x0c, mag_mode=0x16):
        self.MPU6050 = MPU6050(acc_address, accel_fsr, gyro_fsr, sample_rate_divider, digital_lowpass_level, ext_sync_set)
        self.AK8963 = AK8963(mag_address, mag_mode)
        
    def get_all_data(self):
        accel_data = self.MPU6050.get_accel_data()
        gyro_data = self.MPU6050.get_gyro_data()
        mag_data = self.AK8963.get_mag_data()
        
        return accel_data, gyro_data, mag_data
    
    def get_heading(self):
        mag_data = self.AK8963.get_mag_data()
        if mag_data:
            return self.AK8963.calculate_heading(mag_data['x'], mag_data['y'])
        return None
    
    def get_pitch(self, samples=100):
        datas = []
        for _ in range(samples):
            data = self.MPU6050.get_accel_data()
            sum = np.sqrt(data["x"]**2 + data["y"]**2 + data["z"]**2)
            datas.append(np.rad2deg(np.arcsin(data["y"]/sum)))
            
        return np.mean(datas)
        
    
        