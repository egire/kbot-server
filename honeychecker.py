import csv, os, random, struct
import notify

_KBMAP = "p0o9i8u7y6t5r4e3w2q1a!s@d#f$g%h^j&k*(l)mnbvcxz"
_LEET = "4bcd3f6h1jklmn0pqr57uvwxyz"
_NUM = "5482109376"
_SYM = "#^)*(!@&$%"

schema = ['salt', 'index']
    
def addSweetword(salt, index):
    return create(salt, index)
    
    
def notifyHoneyword():
    notify.notify()


def getSweetword(salt):
    return read(salt, 'index')


def validSweetword(salt):
    if getSweetword(salt):
        return True
    else:
        return False


def randomASCII(word, pos=0):
    if pos > len(word):
        pos = len(word)
    ascii = word[0:pos]
    for c in word[pos:]:
        ascii += chr(((ord(c) + struct.unpack('h', os.urandom(2))[0]) % 93)+32) #33-126 ASCII
    return ascii


def randomPassword(file='pws.txt'):
    pwds = []
    
    f = open(file, 'r')
    for line in f:
        pwds.append(line)
    
    word = pwds[random.randint(0, len(pwds)-1)]
    return word


def remap(word, mapping=_LEET):
    mapword = ""
    for c in word:
        mapword += mapping[(ord(c)-ord('a')) % len(mapping)]
    return mapword


def remapNums(word, mapping=_NUM):
    mapword = ""
    for c in word:
        if (c.isdigit()):
            mapword += mapping[(ord(c)-ord('!')) % len(mapping)]
        else:
            mapword += c
    return mapword


def isSym(char):
    if ord(char) == ord('^') or ord(char) == ord('@') or (ord(char) >= ord('!')) and (ord(char) <= ord(')')):
        return True
    else:
        return False

    
def remapSyms(word, mapping=_SYM):
    mapword = ""
    for c in word:
        if (isSym(c)):
            if (c == '^'):
                mapword += '@'
            elif (c == '@'):
                mapword += '^'
            else:
                mapword += mapping[(ord(c)-ord('!')) % len(mapping)]
        else:
            mapword += c
    return mapword


def honeyword(password=""):
    honeyword = ""
    if password:
        honeyword = remap(password)
    yield

    
def create(salt, index):
    global schema
    with open('sweet.db', 'r', newline='\n') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=schema)
        for row in reader:
            if row['salt'] == salt: return False
            
    with open('sweet.db', 'a', newline='\n') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=schema)
        if not os.path.exists('./sweet.db'): writer.writeheader()
        sweetword = {'salt': salt, 'index':index}
        writer.writerow(sweetword)
        return True


def read(salt, field=''):
    global schema
    with open('sweet.db', 'r', newline='\n') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=schema)
        for row in reader:
            if row['salt'] == salt:
                if field:
                    return row[field]
                else:
                    return row
        return None


def update(salt, field='', value=None):
    global schema
    with open('sweet.db', 'r', newline='\n') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=schema)
        
        with open('sweet.tmp', 'w', newline='\n') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=schema)
            for row in reader:
                if row['salt'] == salt:
                    row[field] = value
                    writer.writerow(row)
                else:
                    writer.writerow(row)
    os.remove('sweet.db')
    os.rename('sweet.tmp', 'sweet.db')


def delete(salt):
    global schema
    with open('sweet.db', 'r', newline='\n') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=schema)
        
        with open('sweet.tmp', 'w', newline='\n') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=schema)
            for row in reader:
                if row['salt'] != salt:
                    writer.writerow(row)
    os.remove('sweet.db')
    os.rename('sweet.tmp', 'sweet.db')

if __name__ == "__main__":
    addSweetword("test", 3)
    print(getSweetword("test"))
    delete("test")
    print(getSweetword("test"))
    print(encodeASCII('test', 0))