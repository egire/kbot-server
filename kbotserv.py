import web, json, csv, time, logging
import pin, users

logging.basicConfig(filename='kbot.log', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
        
gStorage = {} # memory storage
gPinConfig = "pins.cfg" # pin config file 
    
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
            out_range = [float(row['out_min']), float(row['out_max'])]
            in_range = [float(row['in_min']), float(row['in_max'])]
            Access_Create(row['name'], row['pin'], row['type'], out_range, in_range)

def Access_Create(pin_name, pin_id, type, out_range, in_range):
    logging.info("Adding Pin ("+ pin_id+")" )
    gStorage[pin_name] = pin.pin(pin_name, pin_id, type, out_range, in_range)

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

def Access_Move(leftFore, rightFore, leftAft, rightAft):
    gStorage['MOTOR'].move(leftFore, rightFore, leftAft, rightAft)

def Access_Sensor(name):
    return gStorage[name].input()

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
    '/json', 'json',
    '/save', 'save',
    '/rotate', 'rotate',
    '/log', 'log',
    '/load', 'load',
    '/login', 'login',
    '/add_user', 'add_user',
    '/move', 'move',
    '/login', 'login',
    '/register', 'register',
    '/sensor', 'sensor',
    '/autonomous', 'autonomous'
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
        if user: return user
        else: return ''
        
class register:
    def POST(self):
        web.header('Content-Type','text/plain; charset=utf-8')
        web.header('Access-Control-Allow-Origin', '*')
        i = web.input(username=None, email=None, password=None)
        success = users.register(i.username, i.password, i.email)
        if (success):
            return 'User registered!'
        else:
            return 'User with this login exists.'

class move:
    def POST(self):
        web.header('Content-Type','text/plain; charset=utf-8')
        web.header('Access-Control-Allow-Origin', '*')
        i = web.input(username=None, token=None, leftFore=None, leftAft=None, rightFore=None, rightAft=None)
        if users.validToken(i.username, i.token):
            Access_Move(float(i.leftFore), float(i.rightFore), float(i.leftAft), float(i.rightAft))
            print(float(i.leftFore), float(i.rightFore), float(i.leftAft), float(i.rightAft))
        else: return ''
        
class add:
    def POST(self):
        web.header('Content-Type','text/plain; charset=utf-8')
        web.header('Access-Control-Allow-Origin', '*')
        i = web.input(username=None, token=None, name=None, pin=None, type=None, min=None, max=None)
        if users.validToken(i.username, i.token):
            range = [i.min, i.max]
            Access_Create(i.name, i.pin, i.type, range) 
            logging.info(str(i.type)+" '" + i.name + "' at pin (" + i.pin + ")")
        else: return ''

class delete:
    def POST(self):
        web.header('Content-Type','text/plain; charset=utf-8')
        web.header('Access-Control-Allow-Origin', '*')
        i = web.input(username=None, token=None, name=None)
        if users.validToken(i.username, i.token):
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
        if users.validToken(i.username, i.token):
            servo = Access_Storage(i.name)
            servo.rotate(int(i.angle))
        else: return ''

class sensor:
    def POST(self):
        web.header('Content-Type','text/plain; charset=utf-8')
        web.header('Access-Control-Allow-Origin', '*')
        i = web.input(username=None, token=None, name=None)
        if users.validToken(i.username, i.token):
            json = '{"t": ' + str(Access_Sensor(i.name)[0]) + ', "y": ' + str(Access_Sensor(i.name)[1]) + '}'
            return json
        else: return ''

class load:
    def POST(self):
        web.header('Content-Type','text/plain; charset=utf-8')
        web.header('Access-Control-Allow-Origin', '*')
        i = web.input(username=None, token=None, name=None)
        if users.validToken(i.username, i.token):
            Access_Load()
            logging.info("Pin configuration loaded.")
        else: return ''

class switch:
    def POST(self):
        web.header('Content-Type','text/plain; charset=utf-8')
        web.header('Access-Control-Allow-Origin', '*')
        i = web.input(username=None, token=None, name=None)
        if users.validToken(i.username, i.token):
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
        if users.validToken(i.username, i.token):
            Access_Autonomous()
            logging.info("Autonomous Mode active.")
        else: return ''
        
class save:
    def POST(self):
        web.header('Content-Type','text/plain; charset=utf-8')
        web.header('Access-Control-Allow-Origin', '*')
        i = web.input(username=None, token=None)
        if users.validToken(i.username, i.token):
            Access_Save()
            logging.info("Pin configuration saved.")
        else: return ''

class log:
    def POST(self):
        web.header('Content-Type','text/plain; charset=utf-8')
        web.header('Access-Control-Allow-Origin', '*')
        i = web.input(username=None, token=None)
        if users.validToken(i.username, i.token):
            i = web.input(tail=None, maxlines=None)
            log = Access_Log(i.tail, int(i.maxlines))
            return log
        else: return ''

class json:
    def POST(self):
        web.header('Content-Type','application/json; charset=utf-8')
        web.header('Access-Control-Allow-Origin', '*')
        i = web.input(username=None, token=None)
        if users.validToken(i.username, i.token):
            json = '['
            for pin, val in gStorage.items():
                json+=str(val)+','
            if len(gStorage) > 0:
                json = json[:-1]
            json += ']'
            return json
        else: return ''

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
    
