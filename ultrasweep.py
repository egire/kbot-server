from sensor import sensor
import RPi.GPIO as GPIO

class sweep:
    def __init__(self, name="Sensor", memsize=10, pin=[]):
        self.sonic = sensor(name, "SONIC", 1, pin[0], self.ping)
        self.sweep = sensor(name, "SWEEP", 1, pin[1], self.sweep)
    
    
    def on(self):
        self.sonic.on()
        self.sweep.on()
    
    
    def off(self):
        self.sonic.off()
        self.sweep.off()
    
    
    def sweep(self, deg=1, rate=0.005, srange=[10.0, 180.0]):
        if not self.state: return
        if(self.type == "SWEEP"):
            sweep = list(range(int(srange[0]), int(srange[1]), deg)) 
            sweep += list(reversed(sweep))
            for i in sweep:
                self.pin.rotate(i)
                self.meta['angle'] = i
                time.sleep(rate)
    
    
    def ping(self):
        if not self.state: return None;
        starttime = time.time()
        endtime = time.time()
        distance = -1
        GPIO.setup(self.pin[0], GPIO.OUT)
        GPIO.output(self.pin[0], 0)
        time.sleep(0.000002)
        GPIO.output(self.pin[0], 1)
        time.sleep(0.000005)
        GPIO.output(self.pin[0], 0)
        GPIO.setup(self.pin[0], GPIO.IN)
        while GPIO.input(self.pin[0])==0:
           starttime=time.time()
        while GPIO.input(self.pin[0])==1:
           endtime=time.time()
        duration=endtime-starttime
        # Distance is defined as time/2 (there and back) * speed of sound 34300 cm/s   
        distance = (duration*34300.0)/2.0
        if self.bad:
            distance += random.uniform(-distance/2.0, distance/2.0)
        time.sleep(0.000001)
        return starttime, distance
    
    
    def reset(self):
        while not self.queue.empty():
            self.queue.get(block=False, timeout=None)
    
    
    def input(self):
        if not self.state: return
        if (self.ping.queue.empty()): return None
        return self.queue.get(block=False, timeout=None)