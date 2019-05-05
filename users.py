import hashlib, uuid, datetime, csv, os, base64, random, logging
import honeychecker#, push

schema = ['username', 'email', 'admin', 'salt', 'token', 'ip']
sweetcount = 6
badactor = False

for i in range(sweetcount):
    schema.append('password'+str(i))

def login(username, password, ip):
    if not exists(username):
        return False
        
    if(validLogin(username, password)):
        user = getUser(username)
        setToken(username)
        setIp(username, ip)
        token = getToken(username)
        return '[{"username":"'+user["username"]+'", "email": "'+user["email"]+'","token":"'+token+'"}]'
    else:
        return False


def register(username, password, email):
    if (exists(username)):
        return False
    else:
        addUser(username, password, email)
        return True


def validLogin(username, password):
    global badactor
    user = getUser(username)
    salt = user["salt"]
    hashpw = hash(password, bytes(salt, 'utf-8'))
    index = honeychecker.getSweetword(salt)
    
    # Not in honeychecker (bad salt, not added to honeychecker?)
    if not honeychecker.validSweetword(salt):
        badactor = True
        return False
    
    # Password from honeychecker database is correct (good actor login)
    if bytes(user["password"+str(index)], 'utf-8') == hashpw[1]:
        badactor = False
        return True
    
    # Password is honeyword (bad actor login)
    honeywords = list(range(sweetcount))
    honeywords.remove(int(index))
    for h in honeywords:
        if bytes(user["password"+str(h)], 'utf-8') == hashpw[1]:
            honeychecker.notifyHoneyword()
            #push.push() push notifications are unreliable 
            badactor = True
            return True
    # Bad login
    return False


def validToken(username, token):
    validToken = getToken(username)
    if token == validToken: return True
    else: return False


def addUser(username, password, email):
    return create(username, password, email)


def exists(username):
    user = getUser(username)
    if (user):
        return True
    else:
        return False


def salt():
    return base64.b64encode(os.urandom(128))


def hash(password, s):
    if not salt:
        s = salt()
    hashpw = base64.b64encode(hashlib.sha256(s+password.encode()).digest())
    return (salt, hashpw)


def token():
    toke = base64.urlsafe_b64encode(os.urandom(32))
    return toke


def setAdmin(isAdmin):
    update(username, "admin", int(isAdmin))
    
    
def getAdmin():
    return float(getUser(userName)["admin"])


def getAdmins():
    return float(getUser(userName)["admin"])


def getPassword(username):
    return getUser(userName)["password"]


def setToken(username):
    tok = token()
    update(username, "token", tok.decode())


def getToken(username):
    tok = token()
    return read(username, "token")


def getIp(username):
    return read(username, "ip")


def setIp(username, ip):
    update(username, "ip", ip)


def getUser(username):
    user = read(username)
    if (user):
        return user
    else:
        return None


def initDB():
    if not os.path.exists('users.db'):
        with open('users.db', 'w+', newline='\n') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=schema)
            writer.writeheader()


def create(username, password, email):
    initDB()
    global schema
    with open('users.db', 'r', newline='\n') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=schema)
        for row in reader:
            if row['username'] == username: return False
    
    with open('users.db', 'a+', newline='\n') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=schema)
        
        s = salt()
        index = random.randint(0, sweetcount-1)
        honeychecker.addSweetword(s.decode(), index)
        user = {'username': username, 'email': email, 'admin': 0, 'token': 0, 'ip': '0.0.0.0'}
        user['salt'] = s.decode()
        
        for hashindex in range(0, sweetcount):
            if hashindex == index:
                user['password'+str(index)] = hash(password, s)[1].decode()
                print(password)
            else:
                genPass = honeychecker.honeyword(password)
                print(genPass)
                user['password'+str(hashindex)] = hash(genPass, s)[1].decode()
        
        writer.writerow(user)
        return True


def read(username, field=""):
    initDB()
    global schema  
    with open('users.db', 'r', newline='\n') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=schema)
        for row in reader:
            if row['username'] == username:
                if field:
                    return row[field]
                else:
                    return row
        return None


def update(username, field="", value=None):
    initDB()
    global schema
    with open('users.db', 'r', newline='\n') as csvfile:
        reader = csv.DictReader(csvfile)
        
        with open('users.tmp', 'w', newline='\n') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=schema)
            writer.writeheader()
            for row in reader:
                if row['username'] == username:
                    row[field] = value
                    writer.writerow(row)
                else:
                    writer.writerow(row)
    os.remove('users.db')
    os.rename('users.tmp', 'users.db')


def delete(username):
    initDB()
    global schema
    with open('users.db', 'r', newline='\n') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=schema)
        
        with open('users.tmp', 'w', newline='\n') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=schema)
            for row in reader:
                if row['username'] != username:
                    writer.writerow(row)
    os.remove('users.db')
    os.rename('users.tmp', 'users.db')

if __name__ == "__main__":
    initDB()
    addUser("test", "test", "test@test.com")
    print(login("test", "pass", "0.0.0.0"))
    delete("test")