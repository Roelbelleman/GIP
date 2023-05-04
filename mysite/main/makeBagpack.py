
from firebase_admin import db
from datetime import datetime

done = True


def makebagpackDone():
    global done
    done = True
    return

def getvergetenBoeken(date,school,username):
    lessen = db.reference('/school/{}/{}/agenda/{}'.format(school,username.replace(".","_"),date)).get()

    scannedBooks = db.reference("/school/{}/{}/scannedBooks".format(school,username.replace(".","_"))).get()    
    lessen = list(lessen.values())
    lessen = list(dict.fromkeys(lessen))
    try:
        scannedBooks = list(dict.fromkeys(scannedBooks))
    except:
        scannedBooks = []
    vergetenBoeken = []

    for x in range(len(lessen)):
        NumberOfKeys = db.reference("/school/{}/{}/keys/{}".format(school,username.replace(".","_"),str(lessen[x]))).get()
        try : NumberOfKeys = len(NumberOfKeys)
        except : NumberOfKeys = 0

        for y in range(NumberOfKeys):
            key = db.reference("/school/{}/{}/keys/{}/{}".format(school,username.replace(".","_"),str(lessen[x]),str(y))).get()
            if key != None:
                vergeten = True
                for y in range(len(scannedBooks)):
                    if(scannedBooks[y] == key):
                        vergeten = False 
                        break
                if(vergeten):
                    vergetenBoeken.append(str(lessen[x]))
    db.reference("/school/{}/{}/scannedBooks".format(school,username.replace(".","_"))).delete()
    vergetenBoeken = count_duplicates(vergetenBoeken)
    return vergetenBoeken

def scanbackpack(school,username):
    db.reference("/school/{}/{}/scannedBooks".format(school,username.replace(".","_"))).delete()
    numberOfScannedbooks = 0
    global done
    done = False
    while(not done):
        scannedKey = db.reference("/scannedKeys/1").get()
        db.reference("/scannedKeys/1").delete()
        if scannedKey != None:
            db.reference("/school/{}/{}/scannedBooks".format(school,username.replace(".","_"))).update({numberOfScannedbooks: scannedKey})
            numberOfScannedbooks = numberOfScannedbooks+1
    return

def count_duplicates(vergetenBoeken):
    new_list = []
    for vak in set(vergetenBoeken):
        count = vergetenBoeken.count(vak)
        if count > 1:
            new_list.append("je vergat " + str(count) + " boeken van " + vak)
        else:
            new_list.append(vak)
    return new_list