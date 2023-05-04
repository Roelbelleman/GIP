import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import datetime

cred = credentials.Certificate("main/serviceAccountKey.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': "https://giproel-3a29d-default-rtdb.europe-west1.firebasedatabase.app/"
}, 'GIPRoel')

x = 1
vakken = []
data = {}

def getNextVak(school, username, current_vak_index, vakken):
    try:
        username = username.replace(".", "_")
        docs = db.reference(f'/school/{school}/{username}/agenda/lessen').get()

        add_vak = False

        while add_vak == False:
            vak = docs[current_vak_index - 1]
            if checkvak(vak, vakken) == False:
                vakken.append(vak)
                add_vak = True
                return vak
            else:
                current_vak_index += 1
    except:
        return "done"



def checkvak(vak, vakken):
    for v in vakken:
        if vak == str(v):
            return True
    return False

def getBoekenCount(vakken, school, username):
    boekenCount = []
    for vak in vakken:
        try:
            aantalBoeken = len(db.reference("/school/{}/{}/keys/{}".format(school, username.replace(".", "_"), vak)).get())
        except:
            aantalBoeken = 0
        boekenCount.append(aantalBoeken)
    return boekenCount



def voegVakToe(school, username, vak):
    db.reference(f"/scannedKeys/1").delete()
    scanned_ids = db.reference(f"/school/{school}/{username.replace('.', '_')}/keys/{vak}").get()
    try:
        scanned_ids = len(scanned_ids)
    except:
        scanned_ids = 0
        
    while True:
        scanned_key = db.reference(f"/scannedKeys/1").get()
        if scanned_key is not None:
            db.reference(f"/school/{school}/{username.replace('.', '_')}/keys/{vak}").update({scanned_ids: scanned_key})
            break
    return



def verwijderVakken(school, username, vak):
    db.reference("scannedKeys/1").delete()

    key_path = f"school/{school}/{username.replace('.', '_')}/keys/{vak}"
    scanned_ids = db.reference(key_path).get() or []
    number_of_scanned_ids = len(scanned_ids)

    if number_of_scanned_ids > 0:
        while True:
            scanned_key = db.reference("scannedKeys/1").get()
            if scanned_key:
                for i in range(number_of_scanned_ids):
                    key_ref = db.reference(f"{key_path}/{i}")
                    if key_ref.get() == scanned_key:
                        key_ref.delete()
                        break
                break
    return

def agenda_weekdag(weekdag,school,username):
    weekdagen = {"maandag": 0, "dinsdag": 1, "woensdag": 2, "donderdag": 3, "vrijdag": 4, "zaterdag": 5, "zondag": 6}

    weekdag_num = weekdagen[weekdag.lower()]

    vandaag = datetime.date.today()
    vandaag_num = vandaag.weekday()

    dagen_verschil = (weekdag_num - vandaag_num) % 7

    if dagen_verschil <= 0:
        dagen_verschil += 7

    weekdag_datum = vandaag + datetime.timedelta(days=dagen_verschil-7)
    print(weekdag_datum.strftime("%Y-%m-%d"))
    path = '/school/{}/{}/agenda/{}'.format(school,username.replace(".","_"),weekdag_datum.strftime("%Y-%m-%d"))
    lessen = db.reference(path).get()
    lessen = list(lessen.values())
    return lessen
