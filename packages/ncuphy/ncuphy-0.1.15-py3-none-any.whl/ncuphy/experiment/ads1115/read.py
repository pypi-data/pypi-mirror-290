class ADS1115:
    def __init__(self, i2c, address=0x48):
        self.i2c = i2c
        self.address = address