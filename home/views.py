#task1 12345
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from  home.models import prof,bloggg,event
import os
from django.core.files.storage import FileSystemStorage
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pickle
import pytz
SCOPES = ["https://www.googleapis.com/auth/calendar"]
#     flow = InstalledAppFlow.from_client_secrets_file('credentials.json', scopes=SCOPES)
#     credentials=flow.run_local_server()
#     pickle.dump(credentials,open("token.pkl","wb"))
#     credentials=pickle.load(open("token.pkl","rb"))


def main(date,st,email):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
        
        #To see list of events in calender:
        # now = datetime.now().isoformat()+"Z"
        # event_result = service.events().list(calendarId="primary", timeMin=now,
        #                                      maxResults=10, singleEvents=True, orderBy="startTime").execute()
        # events = event_result.get('items', [])
        # if not events:
        #     print("No upcoming events")
        # for eve in events:
        #     start = eve["start"].get("dateTime", eve["start"].get("date"))
        #     print(start, eve["summary"])
        # }
        
        # if time and date are not in sting format: 
        # local_timezone = pytz.timezone('Asia/Kolkata')
        # local_offset = timedelta(hours=5, minutes=30)
        # start_time_local = local_timezone.localize(datetime(2023, 7, 1, 9, 0, 0))+local_offset
        # end_time_local = local_timezone.localize(datetime(2023, 7, 1, 14, 0, 0))+local_offset
        
        
        #if time and date are in string format:
        date_string = date
        time_string = st
        # time_stringg = st+timedelta(hours=0,minutes=45)
        # Parse the date and time string
        event_date = datetime.strptime(date_string, '%Y-%m-%d')
        event_time = datetime.strptime(time_string, '%H:%M')
        # eventt_time= datetime.strptime(time_stringg, '%H:%M')
        # Combine the date and time into a single datetime object
        event_datetime = datetime.combine(event_date.date(), event_time.time())
        event_datetime1=datetime.combine(event_date.date(), event_time.time())
        # Set the start and end times in the local time zone (Asia/Kolkata)
        local_timezone = 'Asia/Kolkata'
        start_time_local = event_datetime + timedelta(hours=5, minutes=30)
        end_time_local = event_datetime1 + timedelta(hours=5, minutes=75)
        
        # Convert the start and end times to UTC
        start_time_utc = start_time_local.astimezone(pytz.utc)
        end_time_utc = end_time_local.astimezone(pytz.utc)
        event = {
            'summary': 'Appoitment with patient',
            'location': 'Hospital ABC',
            'description': 'Health Issues',
            'start': {
                'dateTime': start_time_utc.isoformat(),
                'timeZone': 'Asia/Kolkata',
            },
            'end': {
                'dateTime': end_time_utc.isoformat(),
                'timeZone': 'Asia/Kolkata',
            },
            # 'recurrence': [
            #     'RRULE:FREQ=DAILY;COUNT=2'
            # ],
            # 'attendees': [
            #     {'email': 'lpage@example.com'},
            #     {'email': 'sbrin@example.com'},
            # ],
            # 'reminders': {
            #     'useDefault': False,
            #     'overrides': [
            #         {'method': 'email', 'minutes': 24 * 60},
            #         {'method': 'popup', 'minutes': 10},
            #     ],
            # },
        }
        # generate event at specfic email id:
        eve = service.events().insert(calendarId=email, body=event).execute()
        
        # generate event on developer email id:
        # eve = service.events().insert(calendarId="primary", body=event).execute()
        # print(f'jfjsdj'%{eve.get('htmlLink')})

    except HttpError as err:
        print(err)
    
# Create your views here.
def loginn(request):
    if request.method=='POST':
        namee=request.POST['namey']
        pass1=request.POST['passwordd']
        userr=authenticate(username=namee,password=pass1)
        if userr is not None:
            myprof=prof.objects.filter(uname=namee).first()
            cont={'myprof':myprof}
            login(request,userr)
            return redirect('dash')
            # return render(request,f"{myprof.work}.html",cont)
        else:
            return HttpResponse("WRONG CRENDITALS")
            #return render(request,'login.html') 
            # return redirect('fakd_login')            
    
    return render(request,'login.html')    

def signup(request):
    if request.method=='POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        emaill=request.POST['email']
        namee=request.POST['name']
        uploaded_file = request.FILES['document']
        # print(uploaded_file)
        # savefile= FileSystemStorage() 
        # name = savefile.save( namee,uploaded_file)# this is the name of file
        # #know where to save the file
        # print(name)
        # d = os.getcwd() #current directory of the project
        # file_directory = d+'\files\\'+name
        
        pass1=request.POST['password']
        pass2=request.POST['cnfpassword']
        add=request.POST['add']
        d=request.POST.get('doc','off')
        p=request.POST.get('pat','off')
        if pass1!=pass2:
           return HttpResponse("PASSWORD AND CONFRIM PASSWORD DONOT MATCH")
        myuser=User.objects.create_user(namee,emaill,pass1)
        myuser.save()
        print(d,p)
        if d=="on":
            work="doctor"
            myprof=prof(fname=fname,lname=lname,email=emaill,uname=namee,password=pass1,img=uploaded_file,address=add,work=work)
        else:
            work1="patient"
            myprof=prof(fname=fname,lname=lname,email=emaill,uname=namee,password=pass1,img=uploaded_file,address=add,work=work1)   
        myprof.save()       
        return render(request,'login.html') 
        
    return render(request,'signup.html')

def logoutt(request):
    logout(request)
    return render(request,'login.html') 
   
def dash(request):
    namee=request.user.username
    myprof=prof.objects.filter(uname=namee).first()
    papp=event.objects.filter(pso=myprof.sno)
    dapp=event.objects.filter(dso=myprof.sno)
    cont={'myprof':myprof,'papp':papp,'dapp':dapp}
    return render(request,f"{myprof.work}.html",cont)
    
def blog(request):
    user=request.user
    if request.method=='POST':
        title=request.POST['title']
        uploaded_file = request.FILES['docum']
        d=request.POST.get('draftt','off')
        d1=request.POST.get('m1','off')
        d2=request.POST.get('m2','off')
        d3=request.POST.get('m3','off')
        d4=request.POST.get('m4','off')
        summ=request.POST.get('text1','off')
        cont=request.POST.get('text2','off')   
        if d1=="on":
            blogg=bloggg(user=user,title=title,img=uploaded_file,cat="Mental Health",summ=summ,con=cont)
        elif d2=="on":
            blogg=bloggg(user=user,title=title,img=uploaded_file,cat="Heart Disease",summ=summ,con=cont)
        
        elif d3=="on":
            blogg=bloggg(user=user,title=title,img=uploaded_file,cat="Covid-19",summ=summ,con=cont)  
        else:
            blogg=bloggg(user=user,title=title,img=uploaded_file,cat="Immunization",summ=summ,con=cont)  
        print(d1,d2,d3,d4,d)
        if d=="on":
            blogg.draft=True
        else:
            blogg.draft=False 
        blogg.save()
        return redirect('dash')
    return render(request,'blog.html')

def viewd(request):
    userr=request.user
    allPosts=bloggg.objects.filter(user=userr)
    dictt={'allPosts':allPosts}
    return render(request,'blogd.html',dictt)
  
def viewp(request):
    a1=bloggg.objects.filter(draft=False,cat="Mental Health")
    a2=bloggg.objects.filter(draft=False,cat="Heart Disease")
    a3=bloggg.objects.filter(draft=False,cat="Covid-19")
    a4=bloggg.objects.filter(draft=False,cat="Immunization")
    
    dictt={'a1':a1,'a2':a2,'a3':a3,'a4':a4}
    return render(request,'blogp.html',dictt)

def blogpost(request,sno):
    blg=bloggg.objects.filter(sno=sno).first()
    liss={'blg':blg}
    return render(request,'blogpost.html',liss)

def viewdoc(request):
    doct=prof.objects.filter(work="doctor")
    dictt={'doct':doct}
    return render(request,'viewdoc.html',dictt)

def bookapp(request,sno):
    userr=request.user.username
    uss=prof.objects.filter(uname=userr).first()
    psno=uss.sno
    if request.method=='POST':
        special=request.POST['spec']
        date=request.POST['date']  
        stime=request.POST['startt']
        given_time = datetime.strptime(stime, "%H:%M")  # Assuming the given time is in the format HH:MM
        endt= given_time + timedelta(minutes=45)
        obj=prof.objects.filter(sno=sno).first()
        namee=obj.fname+obj.lname
        docemaill=obj.email
        dsno=sno
        evt=event(name=namee,dso=dsno,pso=psno,date=date,stime=stime,endt=endt,special=special)
        evt.save()
        main(date,stime,docemaill)
        return redirect('dash')
    dictt={'sno':sno}
    return render(request,'bookapp.html',dictt)

def chat(request,room_code):
    contextt={'room_code':room_code,'user':request.user.username}
    return render(request,'chat.html',contextt)

# def docchat(request):
#     obj=prof.objects.filter(uname=request.user.username).first()
#     snoo=obj.sno
#     return redirect()
    