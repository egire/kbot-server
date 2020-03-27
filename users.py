import hashlib, csv, os, base64, json
# import honeychecker#, push

schema = ['username', 'email', 'password', 'admin', 'salt', 'token', 'ip']
# sweetcount = 6
# badactor = False
#
# for i in range(sweetcount):
#     schema.append('password'+str(i))


def login(username, password, ip):
    if not exists(username):
        return ''

    if(isValidLogin(username, password)):
        user = getUser(username)
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
    # global badactor
    user = getUser(username)
    salt = user["salt"]
    hashpw = (hash(password, bytes(salt, 'utf-8'))[1]).decode()

    if(user["password"] == hashpw):
        return True

    return False


def isValidToken(username, token):
    isValidToken = getToken(username)
    if token == isValidToken:
        return True
    else:
        return False


def addUser(username, password, email):
    return create(username, password, email)


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
    update(username, "admin", int(isAdmin))


def getAdmin(username):
    return float(getUser(username)["admin"])


def getAdmins(username):
    return float(getUser(username)["admin"])


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


def create(username, password, email):
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

        user = {'username': username, 'email': email, 'admin': 0, 'token': 0, 'ip': '0.0.0.0'}
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
    addUser("test", "test", "test@test.com")
    print(login("test", "pass", "0.0.0.0"))
    delete("test")
