import web, json, csv, time, logging
import pin, users
from adafruit_motorkit import MotorKit

logging.basicConfig(filename='kbot.log', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
        
gStorage = {} # memory storage
gPinConfig = "pins.cfg" # pin config file 
kit = MotorKit()
    
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

def clamp(value=0, min=-1.0, max=1.0):
    if value < min: value = min
    if value > max: value = max
    return value

def Access_Create(pin_name, pin_id, type, range):
    gStorage[pin_name] = pin.pin(pin_name, pin_id, type, range)

def Access_Name(pin_name):
    return gStorage[pin_name].name

def Access_Storage(pin_name):
    return gStorage[pin_name]

def Access_Delete(pin_name):
    gStorage.pop(pin_name)

def Access_Store():
    return gStorage

def Access_Save():
    savePinConfig()

def Access_Load():
    loadPinConfig()

def Access_Move(leftFore, leftAft, rightFore, rightAft):
    kit.motor1.throttle = clamp(leftFore)  #Left Fore
    kit.motor2.throttle = clamp(leftAft)   #Left Aft
    kit.motor3.throttle = clamp(rightFore) #Right Fore
    kit.motor4.throttle = clamp(rightAft)  #Right Aft
    
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

urls = (
    '/add', 'add',
    '/switch', 'switch',
    '/delete', 'delete',
    '/json', 'json',
    '/save', 'save',
    '/rotate', 'rotate',
    '/log', 'log',
    '/load', 'load',
    '/login', 'login',
    '/add_user', 'add_user',
    '/move', 'move',
    '/login', 'login'
)

#webpages
class add_user:
    def POST(self):
        return
        
class login:
    def POST(self):
        web.header('Content-Type','text/plain; charset=utf-8')
        web.header('Access-Control-Allow-Origin', '*')
        i = web.input(username=None, password=None)
        user = users.login(i.username, i.password)
        if user: print(user); return user
        else: return ''

class move:
    def POST(self):
        web.header('Content-Type','text/plain; charset=utf-8')
        web.header('Access-Control-Allow-Origin', '*')
        i = web.input(leftFore=None, leftAft=None, rightFore=None, rightAft=None)
        Access_Move(float(i.leftFore), float(i.leftAft), float(i.rightFore), float(i.rightAft))
        
class add:
    def POST(self):
        i = web.input(name=None, pin=None, type=None, min=None, max=None)
        range = [i.min, i.max]
        Access_Create(i.name, i.pin, i.type, range) 
        logging.info(str(i.type)+" '" + i.name + "' at pin (" + i.pin + ")")

class delete:
    def POST(self):
        i = web.input(name=None)
        item = Access_Storage(i.name) 
        item.output(0)
        Access_Delete(i.name)
        logging.info("Deleted pin (" + i.name + ")")

class rotate:
    def POST(self):
        i = web.input(name=None, angle=None)
        servo = Access_Storage(i.name)
        servo.rotate(int(i.angle))

class load:
    def GET(self):
        Access_Load()
        logging.info("Pin configuration loaded.")

class switch:
    def GET(self):
        i = web.input(name=None)
        io = Access_Storage(i.name)
        if(io.state == 0):
            io.output(1)
            logging.info(i.name + " switched ON")
        elif(io.state == 1):
            io.output(0)
            logging.info(i.name + " switched OFF") 

class save:
    def GET(self):
        Access_Save()
        logging.info("Pin configuration saved.")

class log:
    def GET(self):
        web.header('Content-Type','text/plain; charset=utf-8')
        web.header('Access-Control-Allow-Origin', '*')
        i = web.input(tail=None, maxlines=None)
        log = Access_Log(i.tail, int(i.maxlines))
        return log

class json:
    def GET(self):
        web.header('Content-Type','application/json; charset=utf-8')
        web.header('Access-Control-Allow-Origin', '*')
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
    
