from smbus2 import SMBus
import time
import math
from ..mpu6050 import MPU6050
import numpy as np

class AK8963:
    """
    This class represents the AK8963 magnetometer and provides methods to initialize, calibrate, and read magnetometer data.

    Args:
        address (int): I2C address of the AK8963 sensor (default is 0x0C).
        mode (int): Measurement mode (default is 0x16 for continuous measurement mode 2 with 16-bit output).

    Methods:
        get_mag_data(): Get the magnetometer data in microteslas.
        calculate_heading(x, y): Calculate the heading (direction) based on X and Y magnetometer data.
        calibrate(num_samples): Calibrate the magnetometer to correct hard iron and soft iron distortions.
        apply_calibration(mag_data): Apply the calibration offsets and scales to the raw magnetometer data.
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
        self.calibration = None

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
                mag_data = {'x': x, 'y': y, 'z': z}
                if self.calibration:
                    return self.apply_calibration(mag_data)
                return mag_data

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

    def calibrate(self, num_samples=300):
        """
        Calibrate the magnetometer to correct hard iron and soft iron distortions.

        Args:
            num_samples (int): Number of samples to collect during calibration (default is 300).

        Returns:
            dict: Calibration data including offsets and scaling factors for each axis.
        """
        mag_data = []
        print("Rotate the sensor in all directions to collect calibration data...")

        for _ in range(num_samples):
            data = self.get_mag_data()
            if data:
                mag_data.append(data)
            time.sleep(0.05)

        min_x = min(m['x'] for m in mag_data)
        max_x = max(m['x'] for m in mag_data)
        min_y = min(m['y'] for m in mag_data)
        max_y = max(m['y'] for m in mag_data)
        min_z = min(m['z'] for m in mag_data)
        max_z = max(m['z'] for m in mag_data)

        # Calculate offsets
        offset_x = (max_x + min_x) / 2
        offset_y = (max_y + min_y) / 2
        offset_z = (max_z + min_z) / 2

        # Calculate scale factors
        avg_delta_x = (max_x - min_x) / 2
        avg_delta_y = (max_y - min_y) / 2
        avg_delta_z = (max_z - min_z) / 2

        avg_delta = (avg_delta_x + avg_delta_y + avg_delta_z) / 3

        scale_x = avg_delta / avg_delta_x
        scale_y = avg_delta / avg_delta_y
        scale_z = avg_delta / avg_delta_z

        self.calibration = {
            'offsets': {'x': offset_x, 'y': offset_y, 'z': offset_z},
            'scales': {'x': scale_x, 'y': scale_y, 'z': scale_z}
        }

        print(f"Calibration complete. Offsets: {self.calibration['offsets']}, Scales: {self.calibration['scales']}")
        return self.calibration

    def apply_calibration(self, mag_data):
        """
        Apply the calibration offsets and scales to the raw magnetometer data.

        Args:
            mag_data (dict): Raw magnetometer data.

        Returns:
            dict: Calibrated magnetometer data.
        """
        calibrated_data = {
            'x': (mag_data['x'] - self.calibration['offsets']['x']) * self.calibration['scales']['x'],
            'y': (mag_data['y'] - self.calibration['offsets']['y']) * self.calibration['scales']['y'],
            'z': (mag_data['z'] - self.calibration['offsets']['z']) * self.calibration['scales']['z']
        }
        return calibrated_data


class MPU9250:
    def __init__(self, acc_address=0x68, accel_fsr=2, gyro_fsr=250, sample_rate_divider=1, digital_lowpass_level=0, ext_sync_set=0, mag_address=0x0C, mag_mode=0x16):
        """
        This class combines MPU6050 accelerometer/gyroscope and AK8963 magnetometer to create a full MPU9250 sensor interface.

        Args:
            acc_address (int): I2C address of the MPU6050 (accelerometer/gyroscope) sensor (default is 0x68).
            accel_fsr (int): Accelerometer full scale range (default is 2g).
            gyro_fsr (int): Gyroscope full scale range (default is 250 degrees/second).
            sample_rate_divider (int): Sample rate divider (default is 1).
            digital_lowpass_level (int): Digital low pass filter configuration (default is 0).
            ext_sync_set (int): External sync setting (default is 0).
            mag_address (int): I2C address of the AK8963 magnetometer (default is 0x0C).
            mag_mode (int): Measurement mode for the AK8963 (default is 0x16).
        """
        self.MPU6050 = MPU6050(acc_address, accel_fsr, gyro_fsr, sample_rate_divider, digital_lowpass_level, ext_sync_set)
        self.AK8963 = AK8963(mag_address, mag_mode)
        
    def get_all_data(self):
        """
        Get accelerometer, gyroscope, and magnetometer data from the MPU9250.

        Returns:
            tuple: A tuple containing three dictionaries with accelerometer, gyroscope, and magnetometer data.
        """
        accel_data = self.MPU6050.get_accel_data()
        gyro_data = self.MPU6050.get_gyro_data()
        mag_data = self.AK8963.get_mag_data()
        
        return accel_data, gyro_data, mag_data
    
    def get_heading(self):
        """
        Get the heading based on the magnetometer data.

        Returns:
            float: Heading in degrees relative to magnetic north, or None if data is not available.
        """
        mag_data = self.AK8963.get_mag_data()
        if mag_data:
            return self.AK8963.calculate_heading(mag_data['x'], mag_data['y'])
        return None
    
    def get_pitch(self, samples=100):
        """
        Calculate the pitch angle using accelerometer data.

        Args:
            samples (int): Number of samples to average for pitch calculation (default is 100).

        Returns:
            float: Average pitch angle in degrees.
        """
        datas = []
        for _ in range(samples):
            data = self.MPU6050.get_accel_data()
            total = np.sqrt(data["x"]**2 + data["y"]**2 + data["z"]**2)
            datas.append(np.rad2deg(np.arcsin(data["y"]/total)))
            
        return np.mean(datas)
    
    def calibrate_magnetometer(self, num_samples=300):
        """
        Calibrate the magnetometer using the AK8963's calibration method.

        Args:
            num_samples (int): Number of samples to collect during calibration (default is 300).

        Returns:
            dict: Calibration data including offsets and scaling factors.
        """
        return self.AK8963.calibrate(num_samples)


if __name__ == "__main__":
    # Example usage
    mpu9250 = MPU9250()

    # Calibrate the magnetometer
    mpu9250.calibrate_magnetometer()

    while True:
        accel_data, gyro_data, mag_data = mpu9250.get_all_data()
        heading = mpu9250.get_heading()
        pitch = mpu9250.get_pitch()

        print(f"Accelerometer: {accel_data}")
        print(f"Gyroscope: {gyro_data}")
        print(f"Magnetometer: {mag_data}")
        print(f"Heading: {heading:.2f} degrees")
        print(f"Pitch: {pitch:.2f} degrees\n")

        time.sleep(1)
