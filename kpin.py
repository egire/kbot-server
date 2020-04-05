import RPi.GPIO import GPIO
from adafruit_servokit import ServoKit
import sensor
import json

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
        self.sensor = None
        if (type == "GPIO"):
            if(self.mode == "OUT"):
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(int(self.pin_id), GPIO.OUT)
                GPIO.output(int(self.pin_id), GPIO.HIGH)
            elif(self.mode == "IN"):
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(int(self.pin_id), GPIO.IN)
        elif (type == "PWM"):
            duty_min = 3
            PWM.start(self.pin_id, (100-duty_min), 60.0, 1)
            self.rotate(90)
        elif (type == "SERVO"):
            self.kit = ServoKit(channels=self.channels)
            self.kit.servo[int(self.pin_id)].set_pulse_width_range(0, 3000)
        elif (type == "MOTOR"):
            self.kit = MotorKit()
        elif (type == "SONIC"):
            self.sensor = sensor.sensor(self.name, self.type, 1, [self.pin_id])
        elif (type == "SWEEP"):
            self.kit = ServoKit(channels=self.channels)
            self.kit.servo[int(self.pin_id)].set_pulse_width_range(0, 3000)
            self.sensor = sensor.sensor(self.name, self.type, 1, self)


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
            i = self.sensor.input()
            return i


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
        elif(self.type == "SERVO" or self.type == "SWEEP"):
            self.kit.servo[int(self.pin_id)].angle = angle


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


    def toJSON(self):
        json = {"name": self.name, "type": self.type, "mode": self.mode,
                "pin id": self.pin_id, "state": self.state}
        return json
