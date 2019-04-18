import RPi.GPIO as GPIO
import time
from adafruit_servokit import ServoKit
from adafruit_motorkit import MotorKit

class pin:
    def __init__(self, name="pin1", pin_id=1, type="GPIO", state=0, mode="OUT", out_range=[0,1], in_range=[0,1]):
        self.name = name
        self.type = type
        self.mode = mode
        self.pin_id = int(pin_id)
        self.state = state
        self.out_range = out_range
        self.in_range = in_range
        self.kit = None
        self.channels = 16
        if (type == "GPIO"):
            if(self.mode == "OUT"):
                GPIO.setup(int(self.pin_id), GPIO.OUT)
                GPIO.output(int(self.pin_id), GPIO.HIGH)
            elif(self.mode == "IN"):
                GPIO.setup(int(self.pin_id), GPIO.IN)
        elif (type == "PWM"):
            duty_min = 3
            PWM.start(self.pin_id, (100-duty_min), 60.0, 1)
            self.rotate(90)
        elif (type == "I2C"):
            self.kit = ServoKit(channels=self.channels)
            self.kit.servo[int(self.pin_id)].set_pulse_width_range(0, 3000)
        elif (type == "MOTOR"):
            self.kit = MotorKit()
        elif (type == "SONIC"):
            if(self.mode == "OUT"):
                GPIO.setup(int(self.pin_id), GPIO.OUT)
            elif(self.mode == "IN"):
                GPIO.setup(int(self.pin_id), GPIO.IN)
          
                 
    def output(self, state):
        state = self.clamp(self.state, self.out_range[0], self.out_range[1])
        if(self.type == "GPIO"):
            self.mode = "OUT"
            GPIO.setup(self.pin_id, GPIO.OUT)
            if(state == 1): # HIGH
                self.state = 1
                GPIO.output(self.pin_id, GPIO.HIGH)
            elif(state == 0): # LOW
                self.state = 0
                GPIO.output(self.pin_id, GPIO.LOW)

                 
    def input(self):
        if(self.type == "GPIO"):
            self.mode = "IN"
            GPIO.setup(self.pin_id, GPIO.IN)
            self.state = GPIO.input(self.pin_id)
            return time.time(), self.clamp(self.state, self.in_range[0], self.in_range[1])
        elif(self.type == "SONIC"):
            return self.ping()

                 
    def rotate(self, angle):
        # clamp angle to range
        if (angle < float(self.out_range[0])):
            angle = float(self.out_range[0])
        if (angle > float(self.out_range[1])):
            angle = float(self.out_range[1])
            
        if(self.type == "PWM"):            
            duty_min = 3
            duty_max = 14.5
            duty_span = duty_max - duty_min
            angle_f = float(angle)
            duty = 100 - ((angle_f / 180) * duty_span + duty_min) 
            PWM.set_duty_cycle(self.pin_id, duty)
            self.state = angle_f
        elif(self.type == "I2C"): 
            self.kit.servo[int(self.pin_id)].angle = angle
    
                 
    def ping(self):
        if(self.type == "SONIC"):
            starttime = None
            distance = -1
            GPIO.setup(self.pin_id, GPIO.OUT)
            GPIO.output(self.pin_id, 0)
            time.sleep(0.000002)
            GPIO.output(self.pin_id, 1)
            time.sleep(0.000001)
            GPIO.output(self.pin_id, 0)
            GPIO.setup(self.pin_id, GPIO.IN)
            while GPIO.input(self.pin_id)==0:
               starttime=time.time()
            while GPIO.input(self.pin_id)==1:
               endtime=time.time()
            duration=endtime-starttime
            # Distance is defined as time/2 (there and back) * speed of sound 34300 cm/s   
            distance = (duration*34300.0)/2.0
            time.sleep(0.000001)
            return starttime, distance

                 
    def move(self, leftFore, rightFore, leftAft, rightAft):
        if(self.type == "MOTOR"): 
            self.kit.motor1.throttle = self.clamp(leftFore)  #Left Fore
            self.kit.motor3.throttle = self.clamp(rightFore) #Right Fore
            self.kit.motor2.throttle = self.clamp(leftAft)   #Left Aft
            self.kit.motor4.throttle = self.clamp(rightAft)  #Right Aft
    
                 
    def stop(self):
        if(self.type == "PWM"):
            PWM.stop(self.pin_id)
        elif(self.type == "GPIO"):
            return
             
            
    def clamp(self, value=0.0, min=-1.0, max=1.0):
        if value < min: value = min
        if value > max: value = max
        return value
       
                 
    def __str__(self):
        return '{'+"\"name\":\"{0}\", \"pin\":\"{1}\", \"type\":\"{2}\", \"state\":{3}".format(self.name, self.pin_id, self.type, self.state)+'}'
