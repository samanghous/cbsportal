from django.shortcuts import render,HttpResponse,redirect
from cbs_portal.models import SecurityKeymodel,UserComplaint,UserMessFeedback,NewsEvents
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
import random
# mailing to users
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def securitykeygenerate(request):
    if request.method=='POST':
        email=  request.POST.get("signupemail")   
        domain = email[email.index('@') + 1 : ]
        if str(domain)!="iitg.ac.in":
            messages.warning(request, 'PROVIDE AN IITG EMAIL ADDRESS')
            return redirect("/")
        elif User.objects.filter(email=email).exists():
            messages.warning(request, 'THIS EMAIL ALREADY EXIST!')
            return redirect("/")
        else:
            # generate key
            securitykey = random.randint(100000,999999)
            # save key
            if SecurityKeymodel.objects.filter(email=email).exists():
                currentuser=SecurityKeymodel.objects.filter(email=email).first() 
                currentuser.securitykey=securitykey
                currentuser.save()
            else:
                securitykeyobj=SecurityKeymodel(email=email,securitykey=securitykey)       
                securitykeyobj.save()
            # send mail to user
            subject = 'OTP for CBS Portal registration'
            message = 'Your six digit security key is ' +str(securitykey)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email ,]    
            send_mail( subject, message, email_from, recipient_list )
            # notify user
            messages.success(request, 'Securitykey sent to given Email! KINDLY Register')
            return redirect("/")
    return redirect("/")

    
def index(request):
    if request.method=='POST':
        email=  request.POST.get("signupemail") 
        username=  request.POST.get("signupusername") 
        password=  request.POST.get("signuppassword") 
        securitykey=  request.POST.get("securitykey") 
        domain = email[email.index('@') + 1 : ]
        if str(domain)!="iitg.ac.in":
            messages.warning(request, 'PROVIDE AN IITG EMAIL ADDRESS')
            return redirect("/")
        elif User.objects.filter(username=username).exists():
            messages.warning(request, 'THIS USERNAME ALREADY EXIST!')
            return redirect("/")
        elif User.objects.filter(email=email).exists():
            messages.warning(request, 'THIS EMAIL ALREADY EXIST!')
            return redirect("/")
        else:
            # verify securitykey with user's key
            present=SecurityKeymodel.objects.filter(email=email,securitykey=securitykey)
            if SecurityKeymodel.objects.filter(email=email,securitykey=securitykey).exists():
                # user registration
                user = User.objects.create_user(username, email, password)
                user.save()
                # send registration confirmation mail  
                subject = 'Registration successful! CBS portal'
                message="REGISTRATION SUCCESSFUL AT CBS PORTAL! KINDLY LOGIN. Username:{};Password:{} ".format(username, password)
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email]    
                send_mail( subject, message, email_from, recipient_list )
                # redirect with success message 
                messages.success(request, 'REGISTRATION SUCCESSFUL! KINDLY LOGIN')
                return redirect("/")
            else:
                messages.warning(request,'PLEASE PROVIDE VALID SECURITYKEY')
                return redirect("/")

    newsevents=NewsEvents.objects.all()         
    return render(request,'index.html',{'newsevents':newsevents})    
         

def afterlogin(request): 
    if request.user.is_authenticated:
        usercomplaints=UserComplaint.objects.filter(email=request.user.email) 
        usermessfeed=UserMessFeedback.objects.filter(email=request.user.email)
        newsevents=NewsEvents.objects.all()
        messages.success(request, 'CURRENTLY LOGGEDIN!') 
        return render(request,'afterlogin.html', {'usercomplaints': usercomplaints,'usermessfeed': usermessfeed,'newsevents': newsevents} )
    elif request.method=='POST' :
        uname=  request.POST.get("uname") 
        password=  request.POST.get("password")    
        user = authenticate(username=uname, password=password)
        if user is not None:
            login(request,user)
            # take previous complaints data of user
            usercomplaints=UserComplaint.objects.filter(email=request.user.email)  
            usermessfeed=UserMessFeedback.objects.filter(email=request.user.email)
            newsevents=NewsEvents.objects.all()
            messages.success(request, 'YOU ARE LOGGEDIN!')
            return render(request,'afterlogin.html', {'usercomplaints': usercomplaints,'usermessfeed': usermessfeed,'newsevents': newsevents})
        else:
            messages.warning(request,'PLEASE PROVIDE VALID CREDENTIALS')
            return redirect("/")
    else:
        return redirect("/")  

def afterloginComplaintForm(request): 
    if request.method=='POST' and request.user.is_authenticated:
        hostel=  request.POST.get("hostel") 
        block=  request.POST.get("block") 
        floor=  request.POST.get("floor") 
        roomno=  request.POST.get("roomno") 
        complainttype=  request.POST.get("complainttype") 
        complaint=  request.POST.get("complaint")    
        userComplaintobj=UserComplaint( email=request.user.email,hostel=hostel,block=block,floor=floor,roomno=roomno,cmplnttype=complainttype,complaint=complaint)
        userComplaintobj.save()
        messages.success(request, 'COMPLAINT REGISTERED')
        return redirect("/afterlogin")
    else:
        return redirect("/")    
def afterloginMessFeedForm(request): 
    if request.method=='POST' and request.user.is_authenticated:
        hostel=  request.POST.get("hostel") 
        block=  request.POST.get("block") 
        floor=  request.POST.get("floor")
        hygieneissue =  request.POST.get("hygieneissue")
        hygieneissueTXT=  request.POST.get("hygieneissueTXT")
        qualityissue =  request.POST.get("qualityissue")
        qualityissueTXT=  request.POST.get("qualityissueTXT")
        messrating=  request.POST.get("messrating")
        suggestions=  request.POST.get("suggestions")    
        obj=UserMessFeedback( email=request.user.email,hostel=hostel,block=block,floor=floor,hygieneissue =hygieneissue , hygieneissueTXT=hygieneissueTXT,qualityissue =qualityissue ,qualityissueTXT=qualityissueTXT,messrating=messrating,suggestions=suggestions )
        obj.save()
        messages.success(request, 'MESS FEEDBACK REGISTERED')
        return redirect("/afterlogin")
    else:
        return redirect("/")                  
        
 
        
 
def logoutuser(request):
    logout(request)       
    return redirect("/")           
            
 


 
