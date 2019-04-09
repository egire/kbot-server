import RPi.GPIO as GPIO
import time
from adafruit_servokit import ServoKit

class pin:
    def __init__(self, name, pin_id, type="GPIO", range=[0,1]):
        self.name = name
        self.type = type
        self.pin_id = pin_id
        self.state = 1
        self.range = range
        self.servokit = None
        self.channels = 16
        if (type == "GPIO"):
            GPIO.setup(int(self.pin_id), GPIO.OUT)
            GPIO.output(int(self.pin_id), GPIO.HIGH)
        elif (type == "PWM"):
            duty_min = 3
            PWM.start(self.pin_id, (100-duty_min), 60.0, 1)
            self.rotate(90)
        elif (type == "I2C"):
            self.servokit = ServoKit(channels=self.channels)
            self.servokit.servo[int(self.pin_id)].set_pulse_width_range(0, 3000)

    def output(self, state):
        if(self.type == "GPIO"):
            if(state == 1): # HIGH
                self.state = 1
                GPIO.output(self.pin_id, GPIO.HIGH)
            elif(state == 0): # LOW
                self.state = 0
                GPIO.output(self.pin_id, GPIO.LOW)

    def input(self):
        if(self.type == "GPIO"):
            return self.ping(10)

    def rotate(self, angle):
        # clamp angle to range
        if (angle < self.range[0]):
            angle = self.range[0]
        if (angle > self.range[1]):
            angle = self.range[1]
            
        if(self.type == "PWM"):            
            duty_min = 3
            duty_max = 14.5
            duty_span = duty_max - duty_min
            angle_f = float(angle)
            duty = 100 - ((angle_f / 180) * duty_span + duty_min) 
            PWM.set_duty_cycle(self.pin_id, duty)
            self.state = angle_f
        elif(self.type == "I2C"): 
            self.servokit.servo[int(self.pin_id)].angle = angle
    
    def ping(self, samples):
        if(self.type == "GPIO"):
            GPIO.setup(int(self.pin_id), GPIO.OUT)  
            GPIO.output(int(self.pin_id), 0)  
            time.sleep(0.000002)  
            GPIO.output(int(self.pin_id), 1)  
            time.sleep(0.000001)  
            GPIO.output(int(self.pin_id), 0)  
            GPIO.setup(int(self.pin_id), GPIO.IN)  
            while GPIO.input(int(self.pin_id))==0:  
               starttime=time.time() 
            while GPIO.input(int(self.pin_id))==1:  
               endtime=time.time()
            duration=endtime-starttime  
            # Distance is defined as time/2 (there and back) * speed of sound 34000 cm/s   
            distance=duration*34000/2
            return starttime, distance
    
    def stop():
        if(self.type == "PWM"):
            PWM.stop(self.pin_id)
        elif(self.type == "GPIO"):
            return
        
    def __str__(self):
        return '{'+"\"name\":\"{0}\", \"pin\":\"{1}\", \"type\":\"{2}\", \"state\":{3}".format(self.name, self.pin_id, self.type, self.state)+'}'
