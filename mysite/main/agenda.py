import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta, MO, SA
import time
import urllib.parse


cred = credentials.Certificate("main\serviceAccountKey.json")
firebase_admin.initialize_app(cred, {'databaseURL' : "https://giproel-3a29d-default-rtdb.europe-west1.firebasedatabase.app/"})
PHPSESSID = ""
def agenda(school,username, date):
  
  global PHPSESSID

  lastMonday = date + relativedelta(weekday=MO(-1))
  lastMonday = datetime.combine(lastMonday , datetime.now().time())
  lastMonday = int(time.mktime(lastMonday.timetuple())) - 3600

  nextSaturday = date + relativedelta(weekday=SA(1))
  nextSaturday = datetime.combine(nextSaturday , datetime.now().time())
  nextSaturday = int(time.mktime(nextSaturday.timetuple())) - 3600
  
  url = "https://{}.smartschool.be/index.php?module=Agenda&file=dispatcher".format(school)
  payload = "command=%3Crequest%3E%0A%09%3Ccommand%3E%0A%09%09%3Csubsystem%3Eagenda%3C%2Fsubsystem%3E%0A%09%09%3Caction%3Eget%20lessons%3C%2Faction%3E%0A%09%09%3Cparams%3E%0A%09%09%09%3Cparam%20name%3D%22startDateTimestamp%22%3E%3C!%5BCDATA%5B{}%5D%5D%3E%3C%2Fparam%3E%0A%09%09%09%3Cparam%20name%3D%22endDateTimestamp%22%3E%3C!%5BCDATA%5B{}%5D%5D%3E%3C%2Fparam%3E%0A%09%09%09%3Cparam%20name%3D%22filterType%22%3E%3C!%5BCDATA%5Bfalse%5D%5D%3E%3C%2Fparam%3E%0A%09%09%09%3Cparam%20name%3D%22filterID%22%3E%3C!%5BCDATA%5Bfalse%5D%5D%3E%3C%2Fparam%3E%0A%09%09%09%3Cparam%20name%3D%22gridType%22%3E%3C!%5BCDATA%5B2%5D%5D%3E%3C%2Fparam%3E%0A%09%09%09%3Cparam%20name%3D%22classID%22%3E%3C!%5BCDATA%5B0%5D%5D%3E%3C%2Fparam%3E%0A%09%09%09%3Cparam%20name%3D%22endDateTimestampOld%22%3E%3C!%5BCDATA%5B{}%5D%5D%3E%3C%2Fparam%3E%0A%09%09%09%3Cparam%20name%3D%22forcedTeacher%22%3E%3C!%5BCDATA%5B0%5D%5D%3E%3C%2Fparam%3E%0A%09%09%09%3Cparam%20name%3D%22forcedClass%22%3E%3C!%5BCDATA%5B0%5D%5D%3E%3C%2Fparam%3E%0A%09%09%09%3Cparam%20name%3D%22forcedClassroom%22%3E%3C!%5BCDATA%5B0%5D%5D%3E%3C%2Fparam%3E%0A%09%09%09%3Cparam%20name%3D%22assignmentTypeID%22%3E%3C!%5BCDATA%5B1%5D%5D%3E%3C%2Fparam%3E%0A%09%09%3C%2Fparams%3E%0A%09%3C%2Fcommand%3E%0A%3C%2Frequest%3E".format(lastMonday,nextSaturday,nextSaturday)
  headers = {
    'authority': '{}.smartschool.be'.format(school),
    'accept': '*/*',
    'accept-language': 'nl-BE,nl-NL;q=0.9,nl;q=0.8,en-US;q=0.7,en;q=0.6',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'cookie': 'pid=91a6a8ab-3a7f-4388-8e6b-74947455810e; PHPSESSID={}'.format(PHPSESSID),
    'origin': 'https://{}.smartschool.be'.format(school),
    'pragma': 'no-cache',
    'referer': 'https://{}.smartschool.be/'.format(school),
    'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
  }


  response = requests.request("POST", url, headers=headers, data=payload)


  tree = ET.ElementTree(ET.fromstring(response.text))
  root = tree.getroot()
  courseTitle = root.findall(".//courseTitle")
  date = root.findall(".//date")
  lesuur = root.findall(".//hour")
  
  
  docs = db.reference('/school/{}/{}/lessen'.format(school,username.replace(".","_"))).get()

  if docs == None:
    data ={}
    for x in range(len(courseTitle)):
      data[str(x)] = courseTitle[x].text
    db.reference('/school/{}/{}/agenda/lessen'.format(school,username.replace(".","_"))).set(data)
  Getagenda(school,username,date,lesuur,courseTitle)

def login(username, password, school):
  s = requests.Session()
  response = s.get('https://{}.smartschool.be/'.format(school))
  session_cookies = s.cookies.get_dict()

  username = urllib.parse.quote(username)
  password =  urllib.parse.quote(password)

  url = "https://{}.smartschool.be/login".format(school)

  soup = BeautifulSoup(response.content, features="html.parser")

  generationTime = soup.find("input", {"id": "login_form__generationTime"}).get('value')
  token = soup.find("input", {"id": "login_form__token"}).get('value') 
  payload='login_form%5B_username%5D={}&login_form%5B_password%5D={}&login_form%5B_generationTime%5D={}&login_form%5B_token%5D={}'.format(username,password,generationTime,token)

  headers = {
    'authority': '{}.smartschool.be'.format(school),
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'nl-BE,nl-NL;q=0.9,nl;q=0.8,en-US;q=0.7,en;q=0.6',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded',
    'cookie': 'pid=3abf9059-7124-442c-9517-b906730a0e66; PHPSESSID={}'.format(session_cookies['PHPSESSID']),
    'origin': 'https://{}.smartschool.be'.format(school),
    'pragma': 'no-cache',
    'referer': 'https://{}.smartschool.be/'.format(school),
    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
  }

  response = s.request("POST", url, headers=headers, data=payload)
  session_cookies = s.cookies.get_dict()

  global PHPSESSID
  PHPSESSID = session_cookies['PHPSESSID']
  
  soup = BeautifulSoup(response.text, 'html.parser')
  img_tag = soup.find("img")
  img_src = img_tag["src"]
  db.reference('/school/{}/{}/img/1'.format(school,username.replace(".","_"))).set(img_src)

  agenda(school, username, datetime.now().date())

def Getagenda(school,username,date,lesuur,courseTitle):
  for x in range(len(courseTitle)):
      db.reference('/school/{}/{}/agenda/{}'.format(school,username.replace(".","_"),date[x].text)).update({lesuur[x].text : courseTitle[x].text })

def getImgTag(school,username):
  return str(db.reference('/school/{}/{}/img/1'.format(school,username.replace(".","_"))).get())
