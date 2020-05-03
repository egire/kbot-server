from sensor import sensor
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

class ads:
    def __init__(self, name="ADS", memsize=10, pin=None):
        self.ads = ADS.ADS1015(self.pin.i2c)
        self.chan = AnalogIn(self.ads, pinToAdsChannel(pin.pin_id))
        self.irdistance = sensor(name, "I2C", 1, ads_pin, self.read)
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
        #2.8V at 15cm
        #0.4V at 150cm
        print(self.chan.value, self.chan.voltage)
        return (self.chan.value, self.chan.voltage)

    def reset(self):
        self.irdistance.reset()

    def input(self):
        return self.irdistance.input()

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
