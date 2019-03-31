#import RPi.GPIO as GPIO

class pin:
    def __init__(self, name, pin_id, type="GPIO", range=[0,1]):
        self.name = name
        self.type = type
        self.pin_id = pin_id
        self.state = 1
        self.range = range
        if (type == "GPIO"):
            #GPIO.setup(self.pin_id, GPIO.OUT)
            #GPIO.output(self.pin_id, GPIO.HIGH)
        elif (type == "SERVO"):
            duty_min = 3
            #PWM.start(self.pin_id, (100-duty_min), 60.0, 1)
            self.rotate(90)

    def output(self, state):
        if(self.type == "GPIO"):
            if(state == 1): # HIGH
                self.state = 1
                #GPIO.output(self.pin_id, GPIO.HIGH)
            elif(state == 0): # LOW
                self.state = 0
                #GPIO.output(self.pin_id, GPIO.LOW)

    def rotate(self, angle):
        if(self.type != "SERVO"):
            return
            
        # clamp angle to range
        if (angle < self.range[0]):
            angle = self.range[0]
        if (angle > self.range[1]):
            angle = self.range[1]
            
        duty_min = 3
        duty_max = 14.5
        duty_span = duty_max - duty_min
        angle_f = float(angle)
        duty = 100 - ((angle_f / 180) * duty_span + duty_min) 
        #PWM.set_duty_cycle(self.pin_id, duty)
        self.state = angle_f
        
    def stop():
        if(self.type == "PWM"):
 #           PWM.stop(self.pin_id)
        elif(self.type == "GPIO"):
            return
        
    def __str__(self):
        return '{'+"\"name\":\"{0}\", \"pin\":\"{1}\", \"type\":\"{2}\", \"state\":{3}".format(self.name, self.pin_id, self.type, self.state)+'}'
