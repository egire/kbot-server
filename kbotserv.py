import web, json, csv, time, logging
import kpin
import users
# from cheroot.server import HTTPServer
# #from cheroot.ssl.builtin import BuiltinSSLAdapter
# from cheroot.ssl.pyopenssl import pyOpenSSLAdapter
# import urllib.request

logging.basicConfig(filename='kbot.log', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

gStorage = {} # memory storage
gPinConfig = "pins.cfg" # pin config file
gSweep = False

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

def Access_Create(pin_name, pin_id, type, state, mode, out_range, in_range):
    gStorage[pin_name] = kpin.pin(pin_name, pin_id, type, state, mode, out_range, in_range)

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
    if(len(gStorage) <= 0):
        loadPinConfig()

def Access_Move(leftFore, rightFore, leftAft, rightAft):
    gStorage['MOTOR'].move(leftFore, rightFore, leftAft, rightAft)

def Access_Sensor(name):
    sensor = (Access_Storage(name)).sensor
    return sensor

def Access_Sweep(state):
    ping = Access_Sensor('PING')
    head = Access_Sensor('HEAD')

    if(state):
        head.on()
    else:
        head.off()
    return ''

def Access_Autonomous():
    return ''

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
    '/sweep', 'sweep'
)

#webpages

class login:
    def POST(self):
        web.header('Content-Type','text/plain; charset=utf-8')
        web.header('Access-Control-Allow-Origin', '*')
        ip = web.ctx['ip']
        i = web.input(username=None, password=None)
        user = users.login(i.username, i.password, ip)
        if user:
            logging.info("Login: " + i.username + " (" + ip + ")")
            return user
        else:
            logging.info("Bad Login: " + i.username + " (" + ip + ")")
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
            servo = Access_Storage(i.name)
            servo.rotate(float(i.angle))
        else: return ''

class sensor:
    def POST(self):
        web.header('Content-Type','text/plain; charset=utf-8')
        web.header('Access-Control-Allow-Origin', '*')
        i = web.input(username=None, token=None, name=None)
        if users.isValidToken(i.username, i.token):
            sensor = Access_Sensor(i.name)

            if not sensor.state:
                sensor.reset()
                sensor.on()

            inp = None
            while not inp:
                inp = sensor.input()
            json = '{"x": ' + str(inp[0]) + ', "y": ' + str(inp[1]) + '}'
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
        global gSweep
        web.header('Content-Type','text/plain; charset=utf-8')
        web.header('Access-Control-Allow-Origin', '*')
        i = web.input(username=None, token=None)
        if users.isValidToken(i.username, i.token):
            if not gSweep:
                Access_Sweep(True)
                gSweep = True
            else:
                Access_Sweep(False)
                gSweep = False
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
    app = web.application(urls, globals())
    web.config.debug = True
    #certificate = '/home/pi/kbot/kbot-server/cert/cert.pem',
    #private_key = '/home/pi/kbot/kbot-server/cert/privkey.pem'
    #HTTPServer.ssl_adapter = pyOpenSSLAdapter(certificate, private_key)
    #HTTPServer.ssl_adapter = BuiltinSSLAdapter()
    app.run()
