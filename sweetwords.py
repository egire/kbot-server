import csv, os

schema = ['sweetword', 'valid']
    
def addSweetword(sweetword, valid):
    return create(sweetword, valid)

def getSweetword(sweetword):
    return read(sweetword)


def create(sweetword, valid):
    global schema
    with open('sweet.db', 'r', newline='\n') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=schema)
        for row in reader:
            if row[sweetword]: return False
            
    with open('sweet.db', 'a', newline='\n') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=schema)
        if not os.path.exists('./sweet.db'): writer.writeheader()
        sweetword = {sweetword: True}
        writer.writerow(sweetword)
        return True


def read(sweetword, field=""):
    global schema
    with open('sweet.db', 'r', newline='\n') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row[sweetword]:
                if field:
                    return row[field]
                else:
                    return row
        return None


def update(sweetword, field="", value=None):
    global schema
    with open('sweet.db', 'r', newline='\n') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=schema)
        
        with open('sweet.tmp', 'w', newline='\n') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=schema)
            for row in reader:
                if row[sweetword]:
                    row[field] = value
                    writer.writerow(row)
                else:
                    writer.writerow(row)
    os.remove('sweet.db')
    os.rename('sweet.tmp', 'sweet.db')


def delete(sweetword):
    global schema
    with open('sweet.db', 'r', newline='\n') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=schema)
        
        with open('sweet.tmp', 'w', newline='\n') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=schema)
            for row in reader:
                if not row[sweetword]:
                    writer.writerow(row)
    os.remove('sweet.db')
    os.rename('sweet.tmp', 'sweet.db')

if __name__ == "__main__":
    addSweet("sdaho3987hdnasd", True)
    print(getSweetword("sdaho3987hdnasd"))
    delete("sdaho3987hdnasd")