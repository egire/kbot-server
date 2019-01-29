import web
import json
import csv
import time
import logging
import RPi.GPIO as GPIO

logging.basicConfig(filename='kbot.log', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

class pin:
    def __init__(self, name, pin_id, type="GPIO", range=[0,1]):
        self.name = name
        self.type = type
        self.pin_id = pin_id
        self.state = 1
        self.range = range
        if (type == "GPIO"):
            GPIO.setup(self.pin_id, GPIO.OUT)
            GPIO.output(self.pin_id, GPIO.HIGH)
        elif (type == "SERVO"):
            duty_min = 3
            PWM.start(self.pin_id, (100-duty_min), 60.0, 1)
            self.rotate(90)

    def output(self, state):
        if(self.type == "GPIO"):
            if(state == 1): # HIGH
                self.state = 1
                GPIO.output(self.pin_id, GPIO.HIGH)
            elif(state == 0): # LOW
                self.state = 0
                GPIO.output(self.pin_id, GPIO.LOW)

    def rotate(self, angle):
        if(self.type != "SERVO"):
            return
            
        #clamp angle to range
        if (angle < self.range[0]):
            angle = self.range[0]
        if (angle > self.range[1]):
            angle = self.range[1]
            
        duty_min = 3
        duty_max = 14.5
        duty_span = duty_max - duty_min
        angle_f = float(angle)
        duty = 100 - ((angle_f / 180) * duty_span + duty_min) 
        PWM.set_duty_cycle(self.pin_id, duty)
        self.state = angle_f
        
    def stop():
        if(self.type == "PWM"):
            PWM.stop(self.pin_id)
        elif(self.type == "GPIO"):
            return
        
    def __str__(self):
        return '{'+"\"name\":\"{0}\", \"pin\":\"{1}\", \"type\":\"{2}\", \"state\":{3}".format(self.name, self.pin_id, self.type, self.state)+'}'
        
gStorage = {} #memory storage
gPinConfig = "pins.cfg" #pin config file 
    
def savePinConfig():
    with open(gPinConfig, 'w', newline='') as csvfile:
        fieldnames = ['name', 'pin', 'type', 'state', 'range_min', 'range_max']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for pin in gStorage.items():
            writer.writerow({'name':pin[0],'pin':pin[1].pin_id,'state':pin[1].state})

def loadPinConfig():
    with open(gPinConfig, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            range = [int(row['range_min']), int(row['range_max'])]
            Access_Create(row['name'], row['pin'], row['type'], range)

def Access_Create(string, pin_id, type, range):
    gStorage[string] = pin(string, pin_id, type, range)
    logging.info('Loading pin ('+pin_id+') created.')

def Access_Name(string):
    return gStorage[string].name

def Access_Object(string):
    return gStorage[string]

def Access_Delete(string):
    gStorage.pop(string)
    logging.info('Loading pin ('+string+') removed.')

def Access_Store():
    return gStorage

def Access_Save():
    logging.info('Saving pin configuration.')
    savePinConfig()

def Access_Load():
    logging.info('Saving pin configuration.')
    loadPinConfig()
    
def Access_Log(tail=True, maxlines=10):
    log = []
    data = ""
    with open('kbot.log') as file:
        if (tail == "True" or tail == True):
            log = file.readlines()[-1]
            data = "<br>".join(log)
        else:
            log = file.readlines()[-maxlines:]
            data = "<br>".join(log)
    return data

""" Web.py requires us to route the urls and we
need to define them in this urls variable"""

urls = (
    '/add', 'add',
    '/switch', 'switch',
    '/delete', 'delete',
    '/json', 'json',
    '/save', 'save',
    '/rotate', 'rotate',
    '/log', 'log',
    '/load', 'load'
    '/login' ''
)

# Webpage classes

class add_user:
    def PUT(self):

class login:
    def GET(self):
        
        
    
class add:
    def GET(self):
        i = web.input(name=None, pin=None, type=None, state=None, range_min=None, range_max=None) #To get input using the GET request we need to use web.input
        range = [i.range_min, i.range_max]
        Access_Create(i.name, i.pin, i.type, i.state, range) #We are creating an Appliance object with the Access_Create() function
        logging.info("Created a pin: " + i.name + " at pin number: " + i.pin) #logging.info(out the event to the console

class delete:
    def GET(self):
        i = web.input(name=None) #Access the name of the appliance from the url
        item = Access_Object(i.name) #Use Access_Object() function to access the appliance object
        item.output(0) #Turn the Appliance object off
        Access_Delete(i.name) #Delete the Appliance object 
        logging.info("Deleted pin: " + i.name) #logging.info(out the event to the console

class rotate:
    def GET(self):
        i = web.input(name=None, angle=None)
        item = Access_Object(i.name)
        item.rotate(int(i.angle))

class load:
    def GET(self):
        Access_Load()

class switch:
    def GET(self):
        i = web.input(name=None) #Access the name of the appliance from the url
        item = Access_Object(i.name)#Use Access_Object() function to access the appliance object
        if(item.state == 0): #if the item is off turn it on
            item.output(1)
            logging.info(i.name + " is turned ON") #logging.info(out the event on the console
        elif(item.state == 1):#else if the item is on then turn it off
            item.output(0)
            logging.info(i.name + " is turned OFF") #logging.info(event to the console

class save:
    def GET(self):
        Access_Save()
        logging.info("Configuration saved.")

class log:
    def GET(self):
        web.header('Content-Type','application/json; charset=utf-8')
        web.header('Access-Control-Allow-Origin', '*');
        i = web.input(tail=None, maxlines=None)
        log = Access_Log(i.tail, int(i.maxlines))
        return log

class json:
    def GET(self):
        web.header('Content-Type','application/json; charset=utf-8')
        web.header('Access-Control-Allow-Origin', '*');
        json = '['
        for pin, val in gStorage.items():
            json+=str(val)+','
        if len(gStorage) > 0:
            json = json[:-1]
        json += ']'
        return json

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
    
