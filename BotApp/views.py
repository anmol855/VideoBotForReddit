from django.shortcuts import render
from django.contrib import messages
#import video_creation.final_video
from django.http import HttpResponseRedirect
from .forms import SpecForm,LoginForm,CustomSpecForm,VoiceForm,CustomVoiceForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from . models import *
import os
import webapp
from webapp import *
from django.contrib.auth.hashers import make_password
import time
from plyer import notification
import praw
import PIL
import urllib
import datetime
import shutil
import pathlib
from prawcore.exceptions import NotFound
selected_page=""


@login_required(login_url='/')
def index(request):  
        submitted = False
        if request.method == "POST":
                form = SpecForm(request.POST)
                new_form = form.save(commit=False)
                if form.is_valid():
                        #password = form.cleaned_data['REDDIT_PASSWORD']
                        #encryptedpassword=make_password(request.POST['REDDIT_PASSWORD'])
                        #request.POST['REDDIT_PASSWORD']=encryptedpassword
                        #new_form.REDDIT_PASSWORD=encryptedpassword
                        #print(encryptedpassword)
                        #new_form.voice=voicechosen
                        print('formmmmmmmmmmmm',new_form.SELECTED_VOICE)
                        new_form.save()
                        return 	HttpResponseRedirect('/download')	
        else:
                new_form = SpecForm
                if 'submitted' in request.GET:
                        submitted = True
        chk=CustomSpec.objects.all().count()
        if(chk):
                CustomSpec.objects.all().delete()
        items=Spec.objects.all()
        #print(items[items.count()-1].MAX_COMMENT_LENGTH)
        user=login.objects.all()
        username=user[user.count()-1].REDDIT_USERNAME
        file_exists = exists("BotMaker/newdata.txt")
        name_file=""
        count=0
        if(file_exists):
                with open('BotMaker/newdata.txt') as f:
                        lines = f.readlines()
                name_file=lines[0]
                count=1
                os.remove("BotMaker/newdata.txt")
        file_exists1 = exists("BotMaker/datanew.txt")
        name_file1=""
        if(file_exists1):
                with open('BotMaker/datanew.txt') as f1:
                        lines = f1.readlines()
                name_file1=lines[0]
        print(name_file1)
        return render(request, 'index.html', {'form':new_form, 'submitted':submitted,'username':username,'name_file':name_file1,'count':count,'notfile':name_file})
        #name_file=video_creation.final_video.fname()
        #return render(request,"index.html",{"name_file":name_file})
        #return render(request,'index.html', context)#geniusvoice.html
@login_required(login_url='/')
def download(request):
        return render(request,'geniusvoice.html',{})
@login_required(login_url='/')
def videos(request):
        if(customspecvoices.objects.all().count()):
                customspecvoices.objects.all().delete()
        chk=CustomSpec.objects.all().count()
        if(chk):
                CustomSpec.objects.all().delete()
        # folder path
        dir_path = r'BotApp/static'
        # list to store files
        res = []
        timee=[]
        # Iterate directory
        time_path=r'BotApp/Static/'
        for path in os.listdir(dir_path):
                if path[len(path)-1]=='4':
                        res.append(path)
                        f_name = pathlib.Path(time_path+path)
                        m_timestamp = f_name.stat().st_mtime
                        #print('nnnn',m_timestamp)
                        m_time = datetime.datetime.fromtimestamp(m_timestamp)
                        print(m_time)
                        format=m_time
                        timee.append(format)
                        #timee.append(m_time)

        print(res)
        print(len(res))
        print(len(timee))
        #print(timee[0])
        '''x=res[0]
        # create a file path
        f_name = pathlib.Path(r'BotApp/Static/')

        # get modification time
        m_timestamp = f_name.stat().st_mtime

        # convert ti to dd-mm-yyyy hh:mm:ss
        m_time = datetime.datetime.fromtimestamp(m_timestamp)
        print(m_time)'''
        user=login.objects.all()
        username=user[user.count()-1].REDDIT_USERNAME
        file_exists = exists("BotMaker/newdata.txt")
        name_file=""
        count=0
        if(file_exists):
                with open('BotMaker/newdata.txt') as f:
                        lines = f.readlines()
                name_file=lines[0]
                count=1
                os.remove("BotMaker/newdata.txt")
        file_exists1 = exists("BotMaker/datanew.txt")
        name_file1=""
        if(file_exists1):
                with open('BotMaker/datanew.txt') as f1:
                        lines = f1.readlines()
                name_file1=lines[0]
        print(name_file1)
        finalvideodata = zip(res, timee)
        print('zipppedd')
        zipped = list(finalvideodata)
        print("Initial zipped list - ", str(zipped))
        sortedzip = sorted(zipped, key = lambda x: x[1],reverse=True)
        print("final list - ", str(sortedzip))
        return render(request,'videos.html',{'res':res,'timee':timee,'finalvideodata':sortedzip,'username':username,'name_file':name_file1,'count':count,'notfile':name_file})


def user_exists(name):
    reddit = praw.Reddit( 
        client_id="",
        client_secret="",
        user_agent='Username checker', # authentication goes here
        )
    if reddit.redditor(name).id:
        return True
    else:
        return False
from prawcore.exceptions import ResponseException    
def userchk(usr,pas,REDDIT_CLIENT_ID,REDDIT_CLIENT_SECRET):
        reddit = praw.Reddit(
        username=usr,
        password=pas,
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent="failing authentication",
        )
        try:
                print("Authenticated as {}".format(reddit.user.me()))
                redditor = reddit.redditor(usr)
                # fetching the URL of the image
                url = redditor.icon_img
                print('url is',url)
                text_file = open("BotMaker/imageurl.txt", "w")
                text_file.write(url)
                return True
        except ResponseException:
                print("Something went wrong during authentication")
                return False


def signin(request): 
        #removing processed video file
        file_e = exists("BotMaker/datanew.txt")
        if(file_e):
                os.remove("BotMaker/datanew.txt") 
        submitted = False
        if request.method == "POST":
                form = LoginForm(request.POST)
                new_form = form.save(commit=False)
                if form.is_valid():
                        usr=form.cleaned_data['REDDIT_USERNAME']
                        #if(user_exists(usr)):
                                #print('exists')
                        #else:
                                #print('not exists')
                        password = form.cleaned_data['REDDIT_PASSWORD']
                        REDDIT_CLIENT_ID=form.cleaned_data['REDDIT_CLIENT_ID']
                        REDDIT_CLIENT_SECRET=form.cleaned_data['REDDIT_CLIENT_SECRET']
                        if(userchk(usr,password,REDDIT_CLIENT_ID,REDDIT_CLIENT_SECRET)):
                                print('Valid Credentials')
                                encryptedpassword=make_password(request.POST['REDDIT_PASSWORD'])
                                #request.POST['REDDIT_PASSWORD']=encryptedpassword
                                new_form.REDDIT_PASSWORD=encryptedpassword
                                print(encryptedpassword)
                                #us=request.POST.get('REDDIT_USERNAME', None)
                                #ps=request.POST.get('REDDIT_PASSWORD', None)
                                #user, created = User.objects.get_or_create(username=us)
                                #u#ser.set_password(ps)
                               # user.save()
                                #user = authenticate(username=us, password=ps)
                               
                                #print('checking',login(request,user))
                                #user = new_form
                                #user = authenticate(username=user.REDDIT_USERNAME, password=user.REDDIT_PASSWORD)
                                #login(request.POST, user)
                                #print('checking',login(request,user))
                                new_form.save()
                                
                                #messages.add_message(request, messages.INFO, 'Invalideeeeeeeeeeeeeeeeeeeeeeeee')
                                return HttpResponseRedirect('/landingpage')
                        messages.add_message(request, messages.INFO, 'Invalid Username/Password/Client-Id/Client-Secret')
                        return HttpResponseRedirect('/')
                        print('Invalid-Credentials')
        else:
                new_form = LoginForm
                if 'submitted' in request.GET:
                        submitted = True
        #items=Spec.objects.all()
        #print(items[items.count()-1].MAX_COMMENT_LENGTH)
        return render(request, 'signin.html', {'form':new_form, 'submitted':submitted})
        #name_file=video_creation.final_video.fname()
        #return render(request,"index.html",{"name_file":name_file})
        #return render(request,'index.html', context)#geniusvoice.html
@login_required(login_url='/')
def profile(request):
        chk=CustomSpec.objects.all().count()
        if(chk):
                CustomSpec.objects.all().delete()
        items=Spec.objects.all()
        #current specifications
        data={}
        l=login.objects.all()
        data['id']=l[l.count()-1].REDDIT_CLIENT_ID
        data['secret']=l[l.count()-1].REDDIT_CLIENT_SECRET
        data['subreddit']=items[items.count()-1].SUBREDDIT
        data['length']=items[items.count()-1].MAX_COMMENT_LENGTH
        data['selectedvoice']=items[items.count()-1].SELECTED_VOICE
        data['filtertype']=items[items.count()-1].FilterType
        data['backgroundurl']=items[items.count()-1].BACKGROUND_VIDEO_URL
        user=login.objects.all()
        username=user[user.count()-1].REDDIT_USERNAME
        print('data',data)
        #processed videos
        # folder path
        dir_path = r'BotApp/static'
        # list to store files
        res = []
        # Iterate directory
        for path in os.listdir(dir_path):
                if path[len(path)-1]=='4':
                        res.append(path)
        print(res)
        #edit profile
        items=Spec.objects.all()
        data1=items[items.count()-1]
        print('updateprofile')
        print(data1)
        name_file=""
        count=0
        file_exists = exists("BotMaker/newdata.txt")
        if(file_exists):
                with open('BotMaker/newdata.txt') as f:
                        lines = f.readlines()
                name_file=lines[0]
                count=1
                os.remove("BotMaker/newdata.txt")
        file_exists1 = exists("BotMaker/datanew.txt")
        name_file1=""
        if(file_exists1):
                with open('BotMaker/datanew.txt') as f1:
                        lines = f1.readlines()
                name_file1=lines[0]
        print(name_file1)
        with open('BotMaker/imageurl.txt') as f2:
                l = f2.readlines()
        url_img=""
        url_img=l[0]
        print(url_img)
        print(type(url_img))
        form = SpecForm(request.POST or None,request.FILES or None,instance=data1)
        if form.is_valid():
                form.save()
                return HttpResponseRedirect('/profile')
        return render(request,'profile.html',{'url_img':url_img,'username':username,'data':data,'res':res,'form':form,'name_file':name_file1,'count':count,'notfile':name_file})
@login_required(login_url='/')
def currentprofile(request):
        items=Spec.objects.all()
        data=items[items.count()-1]
        user=login.objects.all()
        username=user[user.count()-1].REDDIT_USERNAME
        return render(request,'profile.html',{'username':username,'data':data})
@login_required(login_url='/')
def processedvideo(request):
        chk=CustomSpec.objects.all().count()
        if(chk):
                CustomSpec.objects.all().delete()
        file_exists = exists("BotMaker/data.txt")
        #f1= open("BotMaker/new.txt","w+")
        name_file=""
        t=0
        user=login.objects.all()
        username=user[user.count()-1].REDDIT_USERNAME
        if(file_exists):
                with open('BotMaker/data.txt') as f:
                        lines = f.readlines()
                name_file=lines[0]
                #f1.write(name_file)
                t=1
                os.remove("BotMaker/data.txt")
        file_exists = exists("BotMaker/newdata.txt")
        name_file1=""
        count=0
        if(file_exists):
                with open('BotMaker/newdata.txt') as f:
                        lines = f.readlines()
                name_file1=lines[0]
                count=1
                os.remove("BotMaker/newdata.txt")
        file_exists2 = exists("BotMaker/datanew.txt")
        n=""
        if(file_exists2):
                with open('BotMaker/datanew.txt') as f1:
                        lines1=f1.readlines()
                n=lines1[0]
                print('inside',n)
        print('testing',n)
        return render(request,'processedvideo.html',{'name_file':n,'username':username,'count':count,'name_file1':name_file1,'notfile':name_file1})
@login_required(login_url='/')
def updateprofile(request):
        chk=CustomSpec.objects.all().count()
        if(chk):
                CustomSpec.objects.all().delete()
        items=Spec.objects.all()
        data=items[items.count()-1]
        print('updateprofile')
        print(data)
        form = SpecForm(request.POST or None,request.FILES or None,instance=data)
        if form.is_valid():
                form.save()
                return redirect('profile')
        return render(request, 'profile.html',{'data': data,'form':form})   
@login_required(login_url='/')     
def home(request):
        chk=CustomSpec.objects.all().count()
        if(chk):
                CustomSpec.objects.all().delete()
        file_exists = exists("BotMaker/data.txt")
        #f1= open("BotMaker/new.txt","w+")
        name_file=""
        t=0
        user=login.objects.all()
        username=user[user.count()-1].REDDIT_USERNAME
        if(file_exists):
                with open('BotMaker/data.txt') as f:
                        lines = f.readlines()
                name_file=lines[0]
                #f1.write(name_file)
                t=1
                os.remove("BotMaker/data.txt")
        file_exists = exists("BotMaker/newdata.txt")
        name_file1=""
        count=0
        if(file_exists):
                with open('BotMaker/newdata.txt') as f:
                        lines = f.readlines()
                name_file1=lines[0]
                count=1
                os.remove("BotMaker/newdata.txt")
        file_exists2 = exists("BotMaker/datanew.txt")
        n=""
        if(file_exists2):
                with open('BotMaker/datanew.txt') as f1:
                        lines1=f1.readlines()
                n=lines1[0]
                print('inside',n)
        print('testing',n)
        return render(request,'home.html',{'name_file':n,'username':username,'count':count,'name_file1':name_file1,'notfile':name_file1})
        #return render(request,'home.html',{})
def test(request):
        return render(request,'test.html',{})

def page():
        return selected_page
@login_required(login_url='/')
def customindex(request):  
        submitted = False
        if request.method == "POST":
                #print(voices.objects.all().count())
                #print('xxxxxxxxxxxxx',voices.objects.all().count())
                #x=voices.objects.all()
                #voicechosen=x[x.count()-1].FilterType
                form = CustomSpecForm(request.POST)
                #voicechosen=""
                new_form = form.save(commit=False)
                if form.is_valid():
                        #password = form.cleaned_data['REDDIT_PASSWORD']
                        #encryptedpassword=make_password(request.POST['REDDIT_PASSWORD'])
                        #request.POST['REDDIT_PASSWORD']=encryptedpassword
                        #new_form.REDDIT_PASSWORD=encryptedpassword
                        #print(encryptedpassword)add-on
                        #new_form.voice=voicechosen
                        print('cssssssssssssss',new_form.SELECTED_VOICE)
                        new_form.flag=1
                        new_form.save()
                        return 	HttpResponseRedirect('/download')	
        else:
                new_form = CustomSpecForm
                if 'submitted' in request.GET:
                        submitted = True
        items=Spec.objects.all()
        #print(items[items.count()-1].MAX_COMMENT_LENGTH)
        user=login.objects.all()
        username=user[user.count()-1].REDDIT_USERNAME
        file_exists = exists("BotMaker/newdata.txt")
        name_file=""
        count=0
        if(file_exists):
                with open('BotMaker/newdata.txt') as f:
                        lines = f.readlines()
                name_file=lines[0]
                count=1
                os.remove("BotMaker/newdata.txt")
        file_exists1 = exists("BotMaker/datanew.txt")
        name_file1=""
        if(file_exists1):
                with open('BotMaker/datanew.txt') as f1:
                        lines = f1.readlines()
                name_file1=lines[0]
        print(name_file1)
        return render(request, 'customindex.html', {'form':new_form, 'submitted':submitted,'username':username,'name_file':name_file1,'count':count,'notfile':name_file})
        #name_file=video_creation.final_video.fname()
        #return render(request,"index.html",{"name_file":name_file})
        #return render(request,'index.html', context)#geniusvoice.html

@login_required(login_url='/')
def voices(request):  
        submitted = False
        if request.method == "POST":
                form = CustomVoiceForm(request.POST)
                new_form = form.save(commit=False)
                if form.is_valid():
                        #password = form.cleaned_data['REDDIT_PASSWORD']
                        #encryptedpassword=make_password(request.POST['REDDIT_PASSWORD'])
                        #request.POST['REDDIT_PASSWORD']=encryptedpassword
                        #new_form.REDDIT_PASSWORD=encryptedpassword
                        #print(encryptedpassword)add-on
                        #new_form.flag=1
                        #new_form.available_voices="custom"
                        new_form.save()
                        return 	HttpResponseRedirect('/customindex')	
        else:
                new_form = VoiceForm
                if 'submitted' in request.GET:
                        submitted = True
        items=Spec.objects.all()
        #print(items[items.count()-1].MAX_COMMENT_LENGTH)
        user=login.objects.all()
        username=user[user.count()-1].REDDIT_USERNAME
        file_exists = exists("BotMaker/newdata.txt")
        name_file=""
        count=0
        if(file_exists):
                with open('BotMaker/newdata.txt') as f:
                        lines = f.readlines()
                name_file=lines[0]
                count=1
                os.remove("BotMaker/newdata.txt")
        file_exists1 = exists("BotMaker/datanew.txt")
        name_file1=""
        if(file_exists1):
                with open('BotMaker/datanew.txt') as f1:
                        lines = f1.readlines()
                name_file1=lines[0]
        print(name_file1)
        dir_path = r'BotApp/static'
        voc = []
        # Iterate directory
        for path in os.listdir(dir_path):
                if path[len(path)-1]=='3':
                        voc.append(path)
        print(voc)
        return render(request, 'voices.html', {'voc':voc,'form':new_form, 'submitted':submitted,'username':username,'name_file':name_file1,'count':count,'notfile':name_file})
@login_required(login_url='/')
def subredditvoices(request):  
        submitted = False
        if(customspecvoices.objects.all().count()):
                customspecvoices.objects.all().delete()
        if request.method == "POST":
                form = VoiceForm(request.POST)
                new_form = form.save(commit=False)
                if form.is_valid():
                        #password = form.cleaned_data['REDDIT_PASSWORD']
                        #encryptedpassword=make_password(request.POST['REDDIT_PASSWORD'])
                        #request.POST['REDDIT_PASSWORD']=encryptedpassword
                        #new_form.REDDIT_PASSWORD=encryptedpassword
                        #print(encryptedpassword)add-on
                        #new_form.flag=1
                        new_form.save()
                        return 	HttpResponseRedirect('/index')	
        else:
                new_form = VoiceForm
                if 'submitted' in request.GET:
                        submitted = True
        items=Spec.objects.all()
        #print(items[items.count()-1].MAX_COMMENT_LENGTH)
        user=login.objects.all()
        username=user[user.count()-1].REDDIT_USERNAME
        file_exists = exists("BotMaker/newdata.txt")
        name_file=""
        count=0
        if(file_exists):
                with open('BotMaker/newdata.txt') as f:
                        lines = f.readlines()
                name_file=lines[0]
                count=1
                os.remove("BotMaker/newdata.txt")
        file_exists1 = exists("BotMaker/datanew.txt")
        name_file1=""
        if(file_exists1):
                with open('BotMaker/datanew.txt') as f1:
                        lines = f1.readlines()
                name_file1=lines[0]
        print(name_file1)
        dir_path = r'BotApp/static'
        voc = []
        # Iterate directory
        for path in os.listdir(dir_path):
                if path[len(path)-1]=='3':
                        voc.append(path)
        print(voc)
        return render(request, 'voices_subreddit.html', {'voc':voc,'form':new_form, 'submitted':submitted,'username':username,'name_file':name_file1,'count':count,'notfile':name_file})


@login_required(login_url='/')
def videosgen(request):
        if(customspecvoices.objects.all().count()):
                customspecvoices.objects.all().delete()
        chk=CustomSpec.objects.all().count()
        if(chk):
                CustomSpec.objects.all().delete()
        # folder path
        dir_path = r'BotApp/static'
        user=login.objects.all()
        username=user[user.count()-1].REDDIT_USERNAME
        file_exists = exists("BotMaker/newdata.txt")
        name_file=""
        count=0
        if(file_exists):
                with open('BotMaker/newdata.txt') as f:
                        lines = f.readlines()
                name_file=lines[0]
                count=1
                os.remove("BotMaker/newdata.txt")
        file_exists1 = exists("BotMaker/datanew.txt")
        name_file1=""
        if(file_exists1):
                with open('BotMaker/datanew.txt') as f1:
                        lines = f1.readlines()
                name_file1=lines[0]
        print(name_file1)
        return render(request,'videosgen.html',{'username':username,'name_file':name_file1,'count':count,'notfile':name_file})

@login_required(login_url='/')
def availtracks(request):
        items=Spec.objects.all()
        #print(items[items.count()-1].MAX_COMMENT_LENGTH)
        user=login.objects.all()
        username=user[user.count()-1].REDDIT_USERNAME
        file_exists = exists("BotMaker/newdata.txt")
        name_file=""
        count=0
        if(file_exists):
                with open('BotMaker/newdata.txt') as f:
                        lines = f.readlines()
                name_file=lines[0]
                count=1
                os.remove("BotMaker/newdata.txt")
        file_exists1 = exists("BotMaker/datanew.txt")
        name_file1=""
        if(file_exists1):
                with open('BotMaker/datanew.txt') as f1:
                        lines = f1.readlines()
                name_file1=lines[0]
        print(name_file1)
        dir_path = r'BotApp/static'
        voc = []
        # Iterate directory
        for path in os.listdir(dir_path):
                if path[len(path)-1]=='3':
                        voc.append(path)
        print(voc)
        return render(request, 'availabletracks.html', {'voc':voc,'username':username,'name_file':name_file1,'count':count,'notfile':name_file})



@login_required(login_url='/')     
def landingpage(request):
        chk=CustomSpec.objects.all().count()
        if(chk):
                CustomSpec.objects.all().delete()
        file_exists = exists("BotMaker/data.txt")
        #f1= open("BotMaker/new.txt","w+")
        name_file=""
        t=0
        user=login.objects.all()
        username=user[user.count()-1].REDDIT_USERNAME
        if(file_exists):
                with open('BotMaker/data.txt') as f:
                        lines = f.readlines()
                name_file=lines[0]
                #f1.write(name_file)
                t=1
                os.remove("BotMaker/data.txt")
        file_exists = exists("BotMaker/newdata.txt")
        name_file1=""
        count=0
        if(file_exists):
                with open('BotMaker/newdata.txt') as f:
                        lines = f.readlines()
                name_file1=lines[0]
                count=1
                os.remove("BotMaker/newdata.txt")
        file_exists2 = exists("BotMaker/datanew.txt")
        n=""
        if(file_exists2):
                with open('BotMaker/datanew.txt') as f1:
                        lines1=f1.readlines()
                n=lines1[0]
                print('inside',n)
        print('testing',n)
        return render(request,'landingpage.html',{'name_file':n,'username':username,'count':count,'name_file1':name_file1,'notfile':name_file1})
        #return render(request,'home.html',{})