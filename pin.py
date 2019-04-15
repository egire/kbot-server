'''import RPi.GPIO as GPIO
import time
from adafruit_servokit import ServoKit
from adafruit_motorkit import MotorKit
'''

class pin:
    def __init__(self, name="pin1", pin_id=1, type="GPIO", out_range=[0,1], in_range=[0,1]):
        self.name = name
        self.type = type
        self.pin_id = pin_id
        self.state = 1
        self.out_range = out_range
        self.in_range = in_range
        self.kit = None
        self.channels = 16
        if (type == "GPIO"):
	    print ''
            #GPIO.setup(int(self.pin_id), GPIO.OUT)
            #GPIO.output(int(self.pin_id), GPIO.HIGH)
        elif (type == "PWM"):
            duty_min = 3
            #PWM.start(self.pin_id, (100-duty_min), 60.0, 1)
            #self.rotate(90)
        elif (type == "I2C"):
	    print ''
            #self.kit = ServoKit(channels=self.channels)
            #self.kit.servo[int(self.pin_id)].set_pulse_width_range(0, 3000)
        elif (type == "MOTOR"):
	    print ''
            #self.kit = MotorKit()
          
                 
    def output(self, state):
        if(self.type == "GPIO"):
            if(state == 1): # HIGH
                self.state = 1
                #GPIO.output(self.pin_id, GPIO.HIGH)
            elif(state == 0): # LOW
                self.state = 0
                #GPIO.output(self.pin_id, GPIO.LOW)

                 
    def input(self):
        if(self.type == "GPIO"):
            return self.ping()

                 
    def rotate(self, angle):
        # clamp angle to range
        if (angle < float(self.range[0])):
            angle = float(self.range[0])
        if (angle > float(self.range[1])):
            angle = float(self.range[1])
            
        if(self.type == "PWM"):            
            duty_min = 3
            duty_max = 14.5
            duty_span = duty_max - duty_min
            angle_f = float(angle)
            duty = 100 - ((angle_f / 180) * duty_span + duty_min) 
            #PWM.set_duty_cycle(self.pin_id, duty)
            self.state = angle_f
        elif(self.type == "I2C"):
            print '' 
            #self.kit.servo[int(self.pin_id)].angle = angle
    
                 
    def ping(self):
        if(self.type == "GPIO"):
            '''GPIO.setup(int(self.pin_id), GPIO.OUT)  
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
            # Distance is defined as time/2 (there and back) * speed of sound 343 m/s   
            distance = duration*343.0/2.0
            if (distance < self.in_range[0] or distance > self.in_range[1]):
                time.sleep(0.000002)
                self.ping()
            return starttime, distance'''
	return ''
                 
    def move(self, leftFore, rightFore, leftAft, rightAft):
        if(self.type == "I2C"): 
	    print ''
	    '''
            self.kit.motor1.throttle = self.clamp(leftFore)  #Left Fore
            self.kit.motor3.throttle = self.clamp(rightFore) #Right Fore
            self.kit.motor2.throttle = self.clamp(leftAft)   #Left Aft
            self.kit.motor4.throttle = self.clamp(rightAft)  #Right Aft'''
    
                 
    def stop():
        if(self.type == "PWM"):
	    print ''
            #PWM.stop(self.pin_id)
        elif(self.type == "GPIO"):
            return ''
             
            
    def clamp(self, value=0.0, min=-1.0, max=1.0):
        if value < min: value = min
        if value > max: value = max
        return value
       
                 
    def __str__(self):
        return '{'+"\"name\":\"{0}\", \"pin\":\"{1}\", \"type\":\"{2}\", \"state\":{3}".format(self.name, self.pin_id, self.type, self.state)+'}'
