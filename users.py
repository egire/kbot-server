import hashlib, uuid, datetime, csv, os, base64

schema = ['username', 'password', 'email', 'salt', 'token']

def login(username, password):
    if(validLogin(username, password)):
        user = getUser(username)
        setToken(username)
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
    user = getUser(username)
    hashpw = hash(password, bytes(user["salt"], 'utf-8'))
    
    if user["username"] == username and bytes(user["password"], 'utf-8') == hashpw[1]:
        return True
    else:
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


def hash(password, salt=b''):
    if not salt:
        salt = base64.b64encode(os.urandom(128))
    hashpw = base64.b64encode(hashlib.sha512(salt+password.encode()).digest())
    return (salt, hashpw)

def token():
    toke = base64.urlsafe_b64encode(os.urandom(32))
    return toke


def getPassword(username):
    return getUser(userName)["password"]

    
def setToken(username):
    tok = token()
    update(username, "token", tok.decode())


def getToken(username):
    tok = token()
    return read(username, "token")


def getUser(username):
    user = read(username)
    if (user):
        return user
    else:
        return None

def create(username, password, email):
    global schema
    with open('users.db', 'r', newline='\n') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=schema)
        for row in reader:
            if row['username'] == username: return False
            
    with open('users.db', 'a', newline='\n') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=schema)
        if not os.path.exists('./users.db'): writer.writeheader()
        saltnhash = hash(password)
        salt = saltnhash[0]
        hashpw = saltnhash[1]
        user = {'username': username, 'password': hashpw.decode(), 'email': email, 'salt': salt.decode(), 'token': 0}
        writer.writerow(user)
        return True


def read(username, field=""):
    global schema
    with open('users.db', 'r', newline='\n') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['username'] == username:
                if field:
                    return row[field]
                else:
                    return row
        return None


def update(username, field="", value=None):
    global schema
    with open('users.db', 'r', newline='\n') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=schema)
        
        with open('users.tmp', 'w', newline='\n') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=schema)
            for row in reader:
                if row['username'] == username:
                    row[field] = value
                    writer.writerow(row)
                else:
                    writer.writerow(row)
    os.remove('users.db')
    os.rename('users.tmp', 'users.db')


def delete(username):
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
    addUser("test", "test", "test@test.com")
    print(login("test", "pass"))
    delete("test")