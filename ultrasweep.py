from sensor import sensor
import RPi.GPIO as GPIO
import time

class ultrasweep:
    def __init__(self, name="ULTRASWEEP", memsize=10, sonic_pin=12, sweep_pin=0):
        self.sonic = sensor(name, "SONIC", 1, sonic_pin, self.ping)
        self.sweep = sensor(name, "SWEEP", 1, sweep_pin, self.sweep)
        self.state = 0
        self.pin = None

    def on(self):
        self.sonic.on()
        self.sweep.on()
        self.state = 1

    def off(self):
        self.sonic.off()
        self.sweep.off()
        self.state = 0

    def sweep(self, deg=1, rate=0.005, srange=[10.0, 180.0]):
        if not self.state: return
        sweep = list(range(int(srange[0]), int(srange[1]), deg))
        sweep += list(reversed(sweep))
        for i in sweep:
            self.sweep.rotate(i)
            self.sweep.meta['angle'] = i
            time.sleep(rate)


    def ping(self):
        if not self.state: return None;
        starttime = time.time()
        endtime = time.time()
        distance = -1
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, 0)
        time.sleep(0.000002)
        GPIO.output(self.pin, 1)
        time.sleep(0.000005)
        GPIO.output(self.pin, 0)
        GPIO.setup(self.pin, GPIO.IN)
        while GPIO.input(self.pin)==0:
           starttime=time.time()
        while GPIO.input(self.pin)==1:
           endtime=time.time()
        duration=endtime-starttime
        # Distance is defined as time/2 (there and back) * speed of sound 34300 cm/s
        distance = (duration*34300.0)/2.0
        time.sleep(0.000001)
        return starttime, distance


    def reset(self):
        self.sonic.reset()


    def input(self):
        if not self.state:
            return None
        return self.sonic.input()
