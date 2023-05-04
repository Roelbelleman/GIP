from django.shortcuts import render,redirect
from .forms import idForm,dateField
from .agenda import *
from .database import *
from .makeBagpack import *
import datetime


username = ""
password =  ""
school = ""
date = datetime.datetime.today().date()
def index(request):

    form = idForm()

    if request.method == 'POST':
        form = idForm(request.POST)
        if form.is_valid():
            global username
            global password 
            global school 
            username = form.cleaned_data['username'].lower()
            password =  form.cleaned_data['password']
            school = form.cleaned_data['school']
            try:
                docs = db.reference('/school/{}/{}'.format(school,username.replace(".","_"))).get()
                login(username , password, school)

                if docs == None:
                    return redirect("scanIDs")
                else:
                    return redirect("home")
            except:
                print("failed")
                return render(request,"index.html",{'form':form})
    else:
        print("failed extra")
        return render(request,"index.html",{'form':form})

vak = ""       
def scanIDs(request):
    global vak 
    vak = getNextVak(school,username)
    if vak == "done" : return redirect("home")
    else : return render(request,"scanIDs.html",{'vak':vak,'img':getImgTag(school,username),'user':username.replace("."," ")})

def home(request):
    try:
        global date
        form = dateField()
        if request.method == 'POST':
            form = dateField(request.POST)
            if form.is_valid():
                date = form.cleaned_data['date_field']
        
        agenda = {"maandag" : agenda_weekdag("maandag",school,username),
                "dinsdag" : agenda_weekdag("dinsdag",school,username),
                "woensdag" : agenda_weekdag("woensdag",school,username),
                "donderdag" : agenda_weekdag("donderdag",school,username),
                "vrijdag" : agenda_weekdag("vrijdag",school,username),
                'form':form, 'img':getImgTag(school,username),'user':username.replace("."," ")
        }
        return render(request,"home.html",agenda)
    except : return redirect("index")

def scanningIDs(request):
    voegVakToe(school,username,vak)
    format = {'vak':vak,'img':getImgTag(school,username),'user':username.replace("."," ")}
    return render(request, "scanedIDs.html",format)


def makebagpack(request):
    scanbackpack(school,username)
    return redirect("makebagpackDoneV")

def makebagpackDoneV(request):
    try:
        global data
        makebagpackDone()
        agenda(school,username,date)
        vergetenBoeken = getvergetenBoeken(date,school,username)
        return render(request, "makebagpackDoneV.html", {'vergetenBoeken' : vergetenBoeken,'img':getImgTag(school,username),'user':username.replace("."," ") })
    except:
        return redirect("home")
    
def Loguot(request):
    global username,school,password
    username = ""
    school = ""
    password = ""
    return redirect("index")

def chageKeys(request):
    try:
        vakken = db.reference('/school/{}/{}/agenda/lessen'.format(school,username.replace(".","_"))).get()
        vakken = list(set(vakken))
        count = getBoekenCount(vakken,school, username)
        print(count)

        return render(request, "chageKeys.html",{'vakken':vakken,'img':getImgTag(school,username),'user':username.replace("."," "), "count": count})
    except: return redirect("index")

def verwijderVak(request, vak):
    verwijderVakken(school, username, vak)
    return redirect("chageKeys")

def voegToe(request, vak):
    voegVakToe(school, username, vak)
    return redirect("chageKeys")

def custom_error_view(request, exception=None):
    return redirect("index")
