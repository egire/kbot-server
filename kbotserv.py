import web, json, csv, time, base64, logging
import pin, users, ultrasonic, ads1115
import notification
from cheroot.server import HTTPServer
from cheroot.ssl.builtin import BuiltinSSLAdapter

logging.basicConfig(filename='kbot.log', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

gStorage = {} # memory storage
gPinConfig = "pins.cfg" # pin config file
gUltrasonic = None
gAds0 = None
gAds1 = None
gAds2 = None
gAds3 = None
gSpeed = 0

def savePinConfig():
    with open(gPinConfig, 'w', newline='') as csvfile:
        fieldnames = ['name', 'pin', 'type', 'mode', 'state', 'range_min', 'range_max']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for pin in gStorage.items():
            writer.writerow({'name':pin['name'],'pin':pin['pin'].pin_id,'state':pin['state'].state, 'mode':pin['mode']})

def loadPinConfig():
    with open(gPinConfig, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            out_range = [float(row['out_min']), float(row['out_max'])]
            in_range = [float(row['in_min']), float(row['in_max'])]
            Access_Create(row['name'], row['pin'], row['type'], row['state'], row['mode'], out_range, in_range)

def Access_Create(pinName, pinId, type, state, mode, outRange, inRange):
    global gStorage
    gStorage[pinName] = pin.pin(pinName, pinId, type, state, mode, outRange, inRange)

def Access_Name(pinName):
    return gStorage[pinName].name

def Access_Storage(pinName):
    return gStorage[pinName]

def Access_Delete(pinName):
    gStorage.pop(pinName)

def Access_Store():
    return gStorage

def Access_Save():
    savePinConfig()

def Access_Load():
    if(len(gStorage) <= 0):
        loadPinConfig()

def Access_Move(leftFore, rightFore, leftAft, rightAft):
    try:
        gStorage['MOTOR'].move(leftFore, rightFore, leftAft, rightAft)
    except:
        print("Error: Accessing move function or storage failure. Loading storage.")
        Access_Load()

def Access_Rotate(name, angle):
    try:
        servo = Access_Storage(name)
        print("{}, {}".format(name, angle))
        servo.rotate(float(angle))
    except:
        print("Error: Accessing rotate function or storage failure. Loading storage.")
        Access_Load()

def Access_Sensor(name):
    try:
        sensor = (Access_Storage(name)).sensor
        return sensor
    except:
        print("Error: Accessing sensor function or storage failure. Loading storage.")
        Access_Load()
        sensor = (Access_Storage(name)).sensor
        return sensor

def Access_Sweep():
    global gUltrasonic
    if gUltrasonic is None:
        ultrasonicPin = Access_Storage("ULTRASONIC")
        gUltrasonic = ultrasonic.ultrasonic("ULTRASONIC", 10, ultrasonicPin);

    if(gUltrasonic.state == False):
        gUltrasonic.on()
    else:
        gUltrasonic.off()
    return ''

def Access_Battery():
    global gAds0

    if gAds0 is None:
        adsPin = Access_Storage("ADS0")
        gAds0 = ads1115.battery("BATTERY", 10, adsPin)

    if not gAds0.state:
        gAds0.reset()
        gAds0.on()

    sensorInput = None
    while sensorInput is None:
        sensorInput = gAds0.input()

    json = '{"x": ' + str(sensorInput[0]) + ', "y": ' + str(sensorInput[1]) + '}'
    return json

def Access_Power():
    global gAds1
    if gAds1 is None:
        adsPin = Access_Storage("ADS1")
        gAds1 = ads1115.power("POWER", 10, adsPin)

    if not gAds1.state:
        gAds1.reset()
        gAds1.on()

    sensorInput = None
    while sensorInput is None:
        sensorInput = gAds1.input()

    json = '{"x": ' + str(sensorInput[0]) + ', "y": ' + str(sensorInput[1]) + '}'
    return json

def Access_Ir():
    global gAds2
    if gAds2 is None:
        adsPin = Access_Storage("ADS2")
        gAds2 = ads1115.irdistance("IRDISTANCE", 10, adsPin)

    if not gAds2.state:
        gAds2.reset()
        gAds2.on()

    sensorInput = None
    while sensorInput is None:
        sensorInput = gAds2.input()

    json = '{"x": ' + str(sensorInput[0]) + ', "y": ' + str(sensorInput[1]) + '}'
    return json

def Access_Cam(name):
    # config file dict of cams, map name to cam
    try:
        with open("/dev/shm/mjpeg/cam.jpg", 'rb') as f:
            data = f.read()
            encoded = "data:image/png;base64,"+str(base64.b64encode(data).decode('ascii'))
            return encoded
    except:
        return ""

def Access_Autonomous():
    return ''

def Access_Log(tail=True, maxlines=10):
    log = []
    data = ""
    try:
        with open('kbot.log') as file:
            if (tail == "True" or tail == True):
                log = file.readlines()[-1]
                data = "<br>".join(log)
            else:
                log = file.readlines()[-maxlines:]
                data = "<br>".join(log)
    except:
        data = "Data file not loading."
    return data

urls = (
    '/add', 'add',
    '/switch', 'switch',
    '/delete', 'delete',
    '/storage', 'storage',
    '/save', 'save',
    '/rotate', 'rotate',
    '/log', 'log',
    '/load', 'load',
    '/move', 'move',
    '/login', 'login',
    '/register', 'register',
    '/sensor', 'sensor',
    '/autonomous', 'autonomous',
    '/sweep', 'sweep',
    '/cam', 'cam',
    '/ir', 'ir',
    '/battery', 'battery',
    '/power', 'power'
)

#webpages
class cam:
    def POST(self):
        web.header('Content-Type','text/plain; charset=utf-8')
        web.header('Access-Control-Allow-Origin', '*')
        i = web.input(username=None, token=None, name=None)
        if users.isValidToken(i.username, i.token):
            return Access_Cam(i.name)
        else: return ''

class login:
    def POST(self):
        web.header('Content-Type','text/plain; charset=utf-8')
        web.header('Access-Control-Allow-Origin', '*')
        ip = web.ctx['ip']
        i = web.input(username=None, password=None)
        user = users.login(i.username, i.password, ip)
        if user:
            if user["admin"]:
                logging.info("Admin Login: " + i.username + " (" + ip + ")")
                notification.SendEmail("Admin Login: " + i.username, "User " + i.username + " has logged in from " + ip)
                #notification.SendDiscord("User " + i.username + " has logged in")
            else:
                logging.info("User Login: " + i.username + " (" + ip + ")")
                notification.SendEmail("User Login: " + i.username, "User " + i.username + " has logged in from " + ip)
            return json.dumps(user)
        else:
            logging.info("Security - Bad Login: " + i.username + " (" + ip + ")")
            notification.SendEmail("Security - Bad Login: " + i.username, "User " + i.username + " has attempted to login from " + ip)
            return ''

class register:
    def POST(self):
        web.header('Content-Type','text/plain; charset=utf-8')
        web.header('Access-Control-Allow-Origin', '*')
        i = web.input(username=None, email=None, password=None)
        success = users.register(i.username, i.password, i.email)
        if (success):
            logging.info("User Registered: " + i.username + " (" + web.ctx['ip'] + ")")
            return 'User registered!'
        else:
            logging.info("Bad Registration: " + i.username + " (" + web.ctx['ip'] + ")")
            return 'User with this login exists.'

class move:
    def POST(self):
        web.header('Content-Type','text/plain; charset=utf-8')
        web.header('Access-Control-Allow-Origin', '*')
        i = web.input(username=None, token=None, leftFore=None, leftAft=None, rightFore=None, rightAft=None)
        if users.isValidToken(i.username, i.token):
            Access_Move(float(i.leftFore), float(i.rightFore), float(i.leftAft), float(i.rightAft))
        else: return ''

class add:
    def POST(self):
        web.header('Content-Type','text/plain; charset=utf-8')
        web.header('Access-Control-Allow-Origin', '*')
        i = web.input(username=None, token=None, name=None, pin=None, type=None, state=None, mode=None, omin=None, omax=None, imin=None, imax=None)
        if users.isValidToken(i.username, i.token):
            orange = [i.omin, i.omax]
            irange = [i.imin, i.imax]
            Access_Create(i.name, i.pin, i.type, i.state, i.mode, orange, irange)
            logging.info(str(i.type)+" '" + i.name + "' at pin (" + i.pin + ")")
        else: return ''

class delete:
    def POST(self):
        web.header('Content-Type','text/plain; charset=utf-8')
        web.header('Access-Control-Allow-Origin', '*')
        i = web.input(username=None, token=None, name=None)
        if users.isValidToken(i.username, i.token):
            item = Access_Storage(i.name)
            item.output(0)
            Access_Delete(i.name)
            logging.info("Deleted pin (" + i.name + ")")
        else: return ''

class rotate:
    def POST(self):
        web.header('Content-Type','text/plain; charset=utf-8')
        web.header('Access-Control-Allow-Origin', '*')
        i = web.input(username=None, token=None, name=None, angle=None)
        if users.isValidToken(i.username, i.token):
            Access_Rotate(i.name, i.angle)
        else: return ''

class sensor:
    def POST(self):
        web.header('Content-Type','text/plain; charset=utf-8')
        web.header('Access-Control-Allow-Origin', '*')
        i = web.input(username=None, token=None, name=None)
        if users.isValidToken(i.username, i.token):
            sensor = None
            if i.name == "ULTRASONIC":
                global gUltrasonic
                if gUltrasonic is None:
                    ultrasonicPin = Access_Storage("ULTRASONIC")
                    gUltrasonic = ultrasonic.ultrasonic("ULTRASONIC", 1, ultrasonicPin)
                sensor = gUltrasonic
            else:
                sensor = Access_Sensor(i.name)

            sensorInput = None

            if not sensor.state:
                sensor.reset()
                sensor.on()

            while sensorInput is None:
                sensorInput = sensor.input()

            json = '{"x": ' + str(sensorInput[0]) + ', "y": ' + str(sensorInput[1]) + '}'
            return json
        else: return ''

class load:
    def POST(self):
        web.header('Content-Type','text/plain; charset=utf-8')
        web.header('Access-Control-Allow-Origin', '*')
        i = web.input(username=None, token=None, name=None)
        if users.isValidToken(i.username, i.token):
            Access_Load()
        else: return ''

class sweep:
    def POST(self):
        global gUltrasweep
        web.header('Content-Type','text/plain; charset=utf-8')
        web.header('Access-Control-Allow-Origin', '*')
        i = web.input(username=None, token=None)
        if users.isValidToken(i.username, i.token):
            Access_Sweep()
        else: return ''

class battery:
    def POST(self):
        web.header('Content-Type','text/plain; charset=utf-8')
        web.header('Access-Control-Allow-Origin', '*')
        i = web.input(username=None, token=None)
        if users.isValidToken(i.username, i.token):
            return Access_Battery()
        else: return ''

class power:
    def POST(self):
        web.header('Content-Type','text/plain; charset=utf-8')
        web.header('Access-Control-Allow-Origin', '*')
        i = web.input(username=None, token=None)
        if users.isValidToken(i.username, i.token):
            return Access_Power()
        else: return ''

class ir:
    def POST(self):
        web.header('Content-Type','text/plain; charset=utf-8')
        web.header('Access-Control-Allow-Origin', '*')
        i = web.input(username=None, token=None)
        if users.isValidToken(i.username, i.token):
            return Access_Ir()
        else: return ''

class switch:
    def POST(self):
        web.header('Content-Type','text/plain; charset=utf-8')
        web.header('Access-Control-Allow-Origin', '*')
        i = web.input(username=None, token=None, name=None)
        if users.isValidToken(i.username, i.token):
            io = Access_Storage(i.name)
            if(io.state == 0):
                io.output(1)
                logging.info(i.name + " switched ON")
            elif(io.state == 1):
                io.output(0)
                logging.info(i.name + " switched OFF")
        else: return ''

class autonomous:
    def POST(self):
        web.header('Content-Type','text/plain; charset=utf-8')
        web.header('Access-Control-Allow-Origin', '*')
        i = web.input(username=None, token=None);
        if users.isValidToken(i.username, i.token):
            Access_Autonomous()
            logging.info("Autonomous Mode active.")
        else: return ''

class save:
    def POST(self):
        web.header('Content-Type','text/plain; charset=utf-8')
        web.header('Access-Control-Allow-Origin', '*')
        i = web.input(username=None, token=None)
        if users.isValidToken(i.username, i.token):
            Access_Save()
            logging.info("Pin configuration saved.")
        else: return ''

class log:
    def POST(self):
        web.header('Content-Type','text/plain; charset=utf-8')
        web.header('Access-Control-Allow-Origin', '*')
        i = web.input(username=None, token=None)
        if users.isValidToken(i.username, i.token):
            i = web.input(tail=None, maxlines=None)
            log = Access_Log(i.tail, int(i.maxlines))
            return log
        else:
            return ''

class storage:
    def POST(self):
        web.header('Content-Type','application/json; charset=utf-8')
        web.header('Access-Control-Allow-Origin', '*')
        i = web.input(username=None, token=None)
        if users.isValidToken(i.username, i.token):
            if(len(gStorage) > 0):
                storage = "["
                for pin_name, pin in gStorage.items():
                    storage += json.dumps(pin.toJSON()) + ", "
                storage = storage[:-2] + "]"
                return storage
            else:
                return '[]'
        return ''


if __name__ == "__main__":
    # web.config.debug = False
    loadPinConfig()

    HTTPServer.ssl_adapter = BuiltinSSLAdapter("/home/pi/kbot.cert",
                                               "/home/pi/kbot.key")
    app = web.application(urls, globals())
    try:
        app.run()
    except:
        print("Error: Error with webserver.")
