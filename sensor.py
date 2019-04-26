import queue, threading, time
import RPi.GPIO as GPIO

class sensor:
    def __init__(self, name="Sensor", type="SONIC", memsize=1, pin=[]):
        self.name = name
        self.type = type
        self.pin = pin
        self.queue = queue.Queue(memsize)
        self.state = False
        self.out = None
        self.inp = None
    
    def on(self):
        if self.state:
            return
        self.state = True
        if not self.out:
            self.out = threading.Thread(target=self.output)
            self.out.start()
        if not self.inp:
            self.inp = threading.Thread(target=self.input)
            self.inp.start()
        
        
    def off(self):
        if not self.state: 
            return
        self.state = False
        self.out.join()
        self.inp.join()
        self.out = None
        self.inp = None
    
    
    def sweep(self, deg=1, rate=0.0001, srange=[10.0, 180.0]):
        if not self.state: return
        if(self.type == "SWEEP"):
            sweep = list(range(int(srange[0]), int(srange[1]), deg)) 
            sweep += list(reversed(sweep))
            for i in sweep:
                if not self.state: break
                self.pin.rotate(i)
                time.sleep(rate)
    
    
    def ping(self):
        if not self.state: return None;
        if(self.type == "SONIC"):
            starttime = None
            endtime = None
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
            time.sleep(0.000001)
            return starttime, distance
            
    
    def output(self):
        if not self.state: return
        if(self.type == "SONIC"):
            while self.state:
                out = self.ping()
                self.queue.put(out)
            self.queue.task_done()
    
    
    def reset(self):
        while not self.queue.empty():
            self.queue.get(block=True, timeout=None)
    
    
    def input(self):
        if not self.state: return
        if(self.type == "SONIC"):
            if (self.queue.empty()): return None
            return self.queue.get(block=True, timeout=None)      
        elif(self.type == "SWEEP"):
            while(self.state):
                self.sweep()