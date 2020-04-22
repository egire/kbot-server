import hashlib, csv, os, base64, json
# import honeychecker#, push

schema = ['username', 'email', 'password', 'admin', 'salt', 'token', 'ip']
# sweetcount = 6
# badactor = False
#
# for i in range(sweetcount):
#     schema.append('password'+str(i))


def login(username, password, ip="0.0.0.0"):
    if not exists(username):
        return ''

    if(isValidLogin(username, password)):
        user = getUser(username)
        if(isAdmin(username)):
            print("Admin")
            setToken(username)
        setIp(username, ip)
        toke = getToken(username)
        safeUser = {'username': user['username'], 'email': user['email'], 'token': toke}
        return json.dumps(safeUser)
    else:
        return ''


def register(username, password, email):
    if (exists(username)):
        return False
    else:
        addUser(username, password, email)
        return True


def isValidLogin(username, password):
    user = getUser(username)
    salt = user["salt"]
    hashpw = (hash(password, bytes(salt, 'utf-8'))[1]).decode()

    if(user["password"] == hashpw):
        return True

    return False


def isValidToken(username, token):
    if token == "0":
        return False

    userToken = getToken(username)
    if token == userToken:
        return True
    elif userToken == 0:
        return False
    else:
        return False

def addUser(username, password, email, admin=0):
    return create(username, password, email, admin)


def exists(username):
    if(username == ''):
        return False

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


def setAdmin(username, isAdmin):
    update(username, "admin", bool(isAdmin))

def isAdmin(username):
    if not exists(username):
        return False

    admin = int(getUser(username)["admin"])
    if admin != 0:
        return True
    else:
        return False

def getPassword(username):
    return getUser(username)["password"]


def setToken(username):
    tok = token()
    update(username, "token", tok.decode())


def getToken(username):
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


def create(username, password, email, admin):
    initDB()
    global schema
    with open('users.db', 'r', newline='\n') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=schema)
        for row in reader:
            if row['username'] == username:
                return False

    with open('users.db', 'a+', newline='\n') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=schema)

        s = salt()

        user = {'username': username, 'email': email, 'admin': admin, 'token': 0, 'ip': '0.0.0.0'}
        user['salt'] = s.decode()
        user['password'] = hash(password, s)[1].decode()

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
    addUser("test", "pass", "test@test.com", 0)
    addUser("testAdmin", "pass", "testadmin@test.com", 1)
    print(login("test", "pass", "0.0.0.0"))
    print(login("testAdmin", "pass", "0.0.0.0"))
    print(isAdmin("test"))
    print(isAdmin("testAdmin"))
    delete("test")
    delete("testAdmin")
