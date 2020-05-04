from sensor import sensor
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import time

class ads1115:
    def __init__(self, name="ADS", memsize=10, pin=None):
        self.init = ADS.ADS1115(pin.i2c)
        self.chan = AnalogIn(self.init, pinToAdsChannel(pin.pin_id))
        self.irdistance = sensor(name, "I2C", memsize, pin, self.read)
        self.state = False
        self.pin = pin

    def on(self):
        self.irdistance.on()
        self.state = True

    def off(self):
        self.irdistance.off()
        self.state = False

    def read(self):
        if not self.state: return
        return ''

    def reset(self):
        self.irdistance.reset()

    def input(self):
        return self.irdistance.input()

class irdistance(ads1115):
    def read(self):
        if not self.state: return
        # 2.79 - 6 in -> 15.24cm
        # 1.88 - 1 ft -> 30.48cm

        now = time.time()

        x = float(self.chan.voltage)
        distance = -16.747*x + 61.964
        return now, distance

class battery(ads1115):
    def read(self):
        if not self.state: return
        # 8.4 VDC = FULL (100%)
        # 6 VDC = EMPTY (0%)

        now = time.time()

        x = float(self.chan.voltage)
        print(x)
        capacity = 41.67*x - 250.0
        if capacity < 0: capacity = 0
        return now, capacity

class power(ads1115):
    def read(self):
        if not self.state: return
        # 5.1 VDC Nominal
        # 4.75 VDC Low Warning

        now = time.time()

        x = float(self.chan.voltage)
        voltage = 285.71*x - 1357.14
        if voltage < 0: voltage = 0
        return now, voltage

def pinToAdsChannel(pin):
    if pin == 0:
        return ADS.P0
    elif pin == 1:
        return ADS.P1
    elif pin == 2:
        return ADS.P2
    elif pin == 3:
        return ADS.P3
    else:
        return None
