from smbus2 import SMBus
import time


class MPU6050:
    """
    This class represents the MPU6050 sensor and provides methods to read accelerometer and gyroscope data.

    Args:
        address (int): I2C address of the MPU6050 sensor (default is 0x68) (0x69 when AD0 is set to high).
        accel_fsr (int): Accelerometer full scale range (default is 2g).
        gyro_fsr (int): Gyroscope full scale range (default is 250 degrees/second).
        sample_rate_divider (int): Sample rate divider (default is 1).
        digital_lowpass_level (int): Digital low pass filter configuration (default is 0).
        ext_sync_set (int): External sync setting (default is 0).

    Raises:
        AssertionError: If any of the input arguments are invalid.

    Methods:
        get_accel_data(): Get the accelerometer data with unit in g.
        get_gyro_data(): Get the gyroscope data with unit of degrees/second.
        
    Attributes:
        PWR_MGMT_1 (int): Power Management register address.
        
        SMPLRT_DIV (int): Sampling Rate Division register address.
        
        CONFIG (int): Frame Synchronization, Digital Low Pass Filter, and Sampling Rate register address.
        GYRO_CONFIG (int): Gyroscope Full Scale Range register address.
        ACCEL_CONFIG (int): Accelerometer Full Scale Range register address.
        
        INT_ENABLE (int): Interrupt Enable register address.
        
        ACCEL_XOUT_H (int): Accelerometer Readings - High Bytes register address for X-axis.
        ACCEL_YOUT_H (int): Accelerometer Readings - High Bytes register address for Y-axis.
        ACCEL_ZOUT_H (int): Accelerometer Readings - High Bytes register address for Z-axis.
        
        GYRO_XOUT_H (int): Gyroscope Readings - High Bytes register address for X-axis.
        GYRO_YOUT_H (int): Gyroscope Readings - High Bytes register address for Y-axis.
        GYRO_ZOUT_H (int): Gyroscope Readings - High Bytes register address for Z-axis.
        
        DLPF_CONFIGS (dict): Dictionary containing Digital Low Pass Filter and Sample Rate configurations.
        GYRO_CONFIGS (dict): Dictionary containing Gyroscope Full Scale Range configurations.
        ACCEL_CONFIGS (dict): Dictionary containing Accelerometer Full Scale Range configurations.
    """

    # Rest of the code...
class MPU6050:
    # Power Management
    PWR_MGMT_1 = 0x6B
    
    # Sampling Rate Division
    SMPLRT_DIV = 0x19
    
    # Frame Synchronization, Digital Low Pass Filter, Sampling Rate
    CONFIG = 0x1A
    
    # Gyroscope Full Scale Range
    GYRO_CONFIG = 0x1B
    
    # Accelerometer Full Scale Range
    ACCEL_CONFIG = 0x1C
    
    # Interrupt Enable
    INT_ENABLE = 0x38
    
    # Accelerometer Readings - High Bytes
    ACCEL_XOUT_H = 0x3B
    ACCEL_YOUT_H = 0x3D
    ACCEL_ZOUT_H = 0x3F
    
    # Gyroscope Readings - High Bytes
    GYRO_XOUT_H = 0x43
    GYRO_YOUT_H = 0x45
    GYRO_ZOUT_H = 0x47

    # Digital Low Pass Filter and Sample Rate Config, units (Hz, Hz, Hz)
    DLPF_CONFIGS = {
        0: {'gyro_bw': 256, 'accel_bw': 260, 'base_rate': 8000},   # DLPF_CFG = 0
        1: {'gyro_bw': 188, 'accel_bw': 184, 'base_rate': 1000},   # DLPF_CFG = 1
        2: {'gyro_bw': 98,  'accel_bw': 94,  'base_rate': 1000},   # DLPF_CFG = 2
        3: {'gyro_bw': 42,  'accel_bw': 44,  'base_rate': 1000},   # DLPF_CFG = 3
        4: {'gyro_bw': 20,  'accel_bw': 21,  'base_rate': 1000},   # DLPF_CFG = 4
        5: {'gyro_bw': 10,  'accel_bw': 10,  'base_rate': 1000},   # DLPF_CFG = 5
        6: {'gyro_bw': 5,   'accel_bw': 5,   'base_rate': 1000},   # DLPF_CFG = 6
        7: {'gyro_bw': None, 'accel_bw': None, 'base_rate': None}  # Reserved
    }
    
    GYRO_CONFIGS = {
        250: 0x00,  # +/- 250 degrees/second
        500: 0x08,  # +/- 500 degrees/second
        1000: 0x10, # +/- 1000 degrees/second
        2000: 0x18  # +/- 2000 degrees/second
    }
    
    ACCEL_CONFIGS = {
        2: 0x00,   # +/- 2g
        4: 0x08,   # +/- 4g
        8: 0x10,   # +/- 8g
        16: 0x18   # +/- 16g
    }

    def __init__(self, address=0x68, accel_fsr=2, gyro_fsr=250, sample_rate_divider=1, digital_lowpass_level=0, ext_sync_set=0):
        valid_accel_fsr = [2, 4, 8, 16]
        assert accel_fsr in valid_accel_fsr, f"accel_fsr {accel_fsr} is not in the list of valid full scale ranges {valid_accel_fsr}"
        
        valid_gyro_fsr = [250, 500, 1000, 2000]
        assert gyro_fsr in valid_gyro_fsr, f"gyro_fsr {gyro_fsr} is not in the list of valid full scale ranges {valid_gyro_fsr}"
        
        valid_dividers = list(range(1, 256))
        assert sample_rate_divider in valid_dividers, f"sample_rate_divider {sample_rate_divider} is not in the list of valid dividers {valid_dividers}"
        
        valid_dlpf_configs = [0, 1, 2, 3, 4, 5, 6]
        assert digital_lowpass_level in valid_dlpf_configs, f"digital_lowpass_config {digital_lowpass_level} is not in the list of valid configurations {valid_dlpf_configs}"

        valid_ext_sync = [0, 1, 2, 3, 4, 5, 6, 7]
        assert ext_sync_set in valid_ext_sync, f"ext_sync_set {ext_sync_set} is not in the list of valid external sync settings {valid_ext_sync}"
        
        self.address = address
        self.bus = SMBus(1) 
        self.accel_fsr = accel_fsr
        self.gyro_fsr = gyro_fsr
        self.sample_rate_divider = sample_rate_divider
        self.digital_lowpass_level = digital_lowpass_level
        self.ext_sync_set = ext_sync_set

        # Wake up the MPU6050
        self.bus.write_byte_data(self.address, MPU6050.PWR_MGMT_1, 0x00)
        time.sleep(0.1)

        # Set the DLPF and EXT_SYNC_SET configuration
        config_value = (self.ext_sync_set << 3) | self.digital_lowpass_level
        self.bus.write_byte_data(self.address, MPU6050.CONFIG, config_value)

        # Set the sample rate divider
        base_rate = MPU6050.DLPF_CONFIGS[self.digital_lowpass_level]['base_rate']
        if base_rate:
            smplrt_div = self.sample_rate_divider - 1
            self.bus.write_byte_data(self.address, MPU6050.SMPLRT_DIV, smplrt_div)
        else:
            raise ValueError(f"Invalid base rate for DLPF configuration {self.digital_lowpass_level}")

        # Set accelerometer full scale range
        self.bus.write_byte_data(self.address, MPU6050.ACCEL_CONFIG, MPU6050.ACCEL_CONFIGS[self.accel_fsr])

        # Set gyroscope full scale range
        self.bus.write_byte_data(self.address, MPU6050.GYRO_CONFIG, MPU6050.GYRO_CONFIGS[self.gyro_fsr])

        # Enable interrupts
        self.bus.write_byte_data(self.address, MPU6050.INT_ENABLE, 0x01)

        # Print the sample rate
        print(f"Sample rate: {base_rate / self.sample_rate_divider:.2f} Hz")
         
    def _read_raw_data(self, addr):
        # Accelero and Gyro values are 16-bit
        high = self.bus.read_byte_data(self.address, addr)
        low = self.bus.read_byte_data(self.address, addr + 1)
        value = (high << 8) | low
        
        # Convert to signed value
        if value > int(2 ** 15):
            value -= 2 ** 16
        return int(value)

    def get_accel_data(self):
        """
        Get the accelerometer data from the MPU6050 sensor with unit in g.

        Returns:
            dict: A dictionary containing the accelerometer data with keys 'x', 'y', and 'z'.
        """
        accel_x = self._read_raw_data(MPU6050.ACCEL_XOUT_H) * (self.accel_fsr / 2 ** 15)
        accel_y = self._read_raw_data(MPU6050.ACCEL_YOUT_H) * (self.accel_fsr / 2 ** 15)
        accel_z = self._read_raw_data(MPU6050.ACCEL_ZOUT_H) * (self.accel_fsr / 2 ** 15)
        return {'x': accel_x, 'y': accel_y, 'z': accel_z}

    def get_gyro_data(self):
        """
        Get the gyroscope data from the MPU6050 sensor with unit of degrees/second.

        Returns:
            dict: A dictionary containing the gyroscope data with keys 'x', 'y', and 'z'.
        """
        gyro_x = self._read_raw_data(MPU6050.GYRO_XOUT_H) * (self.gyro_fsr / 2 ** 15)
        gyro_y = self._read_raw_data(MPU6050.GYRO_YOUT_H) * (self.gyro_fsr / 2 ** 15)
        gyro_z = self._read_raw_data(MPU6050.GYRO_ZOUT_H) * (self.gyro_fsr / 2 ** 15)
        return {'x': gyro_x, 'y': gyro_y, 'z': gyro_z}


if __name__ == "__main__":
    mpu = MPU6050(accel_fsr=2, gyro_fsr=500, sample_rate_divider=1, digital_lowpass_level=6, ext_sync_set=0)  # Example initialization

    while True:
        accel_data = mpu.get_accel_data()
        gyro_data = mpu.get_gyro_data()

        print(f"Accelerometer: {accel_data}")
        print(f"Gyroscope: {gyro_data}\n")

        time.sleep(1)
