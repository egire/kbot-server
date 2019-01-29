import hashlib, uuid, datetime, csv, os
from base64 import b64decode, b64encode

schema = ['username', 'password', 'email', 'salt', 'token']

def login(username, password):
    if(validLogin(username, password)):
        user = getUser(username)
        return (user.username, user.email, user.token)
    else:
        return False


def validLogin(username, password):
    user = getUser(username);
    hashpw = hash(user.salt, password)
    if user.username == username and user.password == hashpw:
        return True
    else:
        return False


def addUser(username, password, email):
    return create(username, password, email)


def hash(salt="", password=""):
    if len(salt):
        salt = os.urandom(128)
    hashpw = b64encode(hashlib.sha512(salt+password.encode()).digest())
    salt = b64encode(salt)
    return (salt, hashpw)


def token(username):
    token = getHash(username)+datetime.now()
    return token


def getPassword(username):
    return getUser(userName).password

    
def setToken(username):
    token = token(username)
    update(username, "token", token)


def getUser(username):
    user = read(username)
    return user


def create(username, password, email):
    global schema
    with open('users.db', 'r', newline='\n') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['username'] == username: return False
            
    with open('users.db', 'a', newline='\n') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=schema)
        writer.writeheader()
        saltnhash = hash(password)
        salt = saltnhash[0]
        hashpw = saltnhash[1]
        user = {'username': username, 'password': hashpw, 'email': email, 'salt': salt, 'token': 0}
        print(user)
        writer.writerow(user)
        return True


def read(username, field=""):
    global schema
    with open('useds.db', newline='\n') as csvfile:
        reader = csv.DictReader(csvfile)
        if field:
            return reader['username'].field
        else:
            return reader['username']


def update(username="", field="", value=None):
    global schema
    with open("tracker.csv", "r", newline='\n') as csvfile:
        reader = csv.DictReader(csvfile)
        
    with open('useds.db', 'w', newline='\n') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=schema)
        for row in reader:
            if row['username'] == username:
                row[field] == value
                writer.writerow(row)
            else:
                writer.writerow(row)


def delele(username):
    global schema
    with open("tracker.csv", "r", newline='\n') as csvfile:
        reader = csv.DictReader(csvfile)
        
    with open('useds.db', 'w', newline='\n') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=schema)
        writer.writeheader() 
        for row in reader:
            if row['username'] != username:
                writer.writerow(row)

if __name__ == "__main__":
    addUser("scnl3", "test", "test@test.com")
    login("scnl3", "test", "test@test.com")