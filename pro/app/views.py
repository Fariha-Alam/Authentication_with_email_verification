from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.template import loader
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
def home(request):
 return render(request, 'home.html')
def reg(request):
 if request.method=='POST':
  name=request.POST.get('username')
  email=request.POST.get('email')
  password=request.POST.get('pass')
  pass1=request.POST.get('pass1')
  print(name)
  if name is not None:
    for i in name:
        if i in ['.','@','/','#']:
            messages.warning(request,"please remove special character")
            return redirect('reg')
    if User.objects.filter(username=name).exists():
         messages.warning(request,"Username exists")
    elif User.objects.filter(email=email).exists():
            messages.warning(request,"Email exists")
    else:
            if password==pass1:
                user=User.objects.create_user(username=name,email=email,password=password)
                user.set_password(password)
                auth_token=str(uuid.uuid4())
                pro_obj=Profile.objects.create(user=user,auth_token=auth_token)
                pro_obj.save()
                send_mail_registration(email,auth_token)
                
        

 return render(request, 'registration.html')

def send_mail_registration(email,auth_token):
    subject='your account authentication link'
    message=f'hi,please click it  http://127.0.0.1:8000/verify/{auth_token}'
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(subject,message,email_from,recipient_list)
def verify(request,auth_token):
    profile_obj=Profile.objects.filter(auth_token=auth_token).first()
    profile_obj.is_verified=True
    profile_obj.save()
    messages.success(request,'congrats')
    return redirect('login')
def token_send(request):
    return render(request,'token_send.html')

def login_view(request):
    if request.method =='POST':
        name=request.POST.get('username')
        password=request.POST.get('pass')
        
        if len(password) ==0:
            messages.warning(request,"no password found")
            return redirect('login_view')
        user = authenticate(username=name, password=password)
        if user:
            prof=Profile.objects.get(user=user)
           
            if prof.is_verified==True:
                login(request,user)
                return redirect('home')
    return render(request,'login.html')   

def Forget_pass(request):
   if request.method=='POST':
       email=request.POST.get('email')
       user_prof=User.objects.get(email=email)
       res_prof=Profile.objects.get(user=user_prof)
       auth_token=res_prof.auth_token
       send_mail_reset(email,auth_token)
       return redirect('success')
   return  render(request,'reset_pass.html')

def send_mail_reset(Email,auth_token):
   subject='your account authentication link'
   message=f'hi,please click it to Reset your account  http://127.0.0.1:8000/reset_pass/{auth_token}'
   email_from =settings.EMAIL_HOST_USER
   recipient_list=[Email]
   send_mail(subject,message,email_from,recipient_list)


def reset_pass(request,auth_token):
    profile_obj=Profile.objects.filter(auth_token=auth_token).first()
    print("auth_token:", auth_token) 
    if profile_obj:
        if request.method=='POST':
            password=request.POST.get('pass')
            pass1=request.POST.get('pass1')
            if password ==pass1:
                user=profile_obj.user
                user.set_password(password)
                user.save()
                messages.success(request,'congrats')
                return redirect('login')
            else:
                messages.success(request,'password not matched')
        context = {
        'profile_obj': profile_obj,
        # Other context variables...
         }
    return render(request,'new_pass.html',context)

