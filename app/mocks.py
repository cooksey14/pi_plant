
class ADS1115Mock:
    def __init__(self, address=0x48, busnum=None, i2c=None, **kwargs):
        # Mock initialization, you can customize this if needed
        pass

    def read_adc(self, channel, gain=1, data_rate=8):
        # Mock the read_adc method, return a dummy value
        return 123  # You can change this value as needed