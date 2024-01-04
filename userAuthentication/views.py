from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login, logout as auth_logout
from userAuthentication.models import CustomUser
from products.models import *
import random
from datetime import datetime, timedelta
from django.core.mail import send_mail

# Create your views here.




def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        return redirect('home')
    else:
        return render(request,'userside/home.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None and user.is_listed == True:
            auth_login(request,user)
            print('em')
            return redirect('home')
        
        else:
            messages.error(request, "invalid password or username") 
            print('password error')
            return render(request, "userside/home.html") 
          
    else:
        print(' error')
        return render(request, "userside/home.html")   
               

def send_6_digit_otp_email(request):
    otp = random.randint(100000, 999999)
    request.session['otp'] = str(otp)
    #calculate otp expiry time
    expiration_time = datetime.now() + timedelta(seconds=60)
    request.session['otp_expiration_time'] = expiration_time.strftime("%Y-%m-%d  %H:%M:%S")

    remaining_time_seconds = max(0,(expiration_time - datetime.now()).total_seconds())

    # send the otp in email
    subject = 'your 6-digit OTP for email verification'
    message = f'Your Email verification OTP: {otp}'
    from_email = 'favasabdulnassar@gmal.com'
    recipient_email = request.session.get('recipient_email')
    recipient_list = [recipient_email]
                      
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

    request.session['otpsecond']=57
    return redirect('otp_verification')


def signup(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        email = request.POST.get('email1')
        phone_number = request.POST.get('phone1')
        password = request.POST.get('password1')
        request.session['recipient_email'] = email
    
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "email is already exists")
            print('email error')
            return render(request,'userside/signup.html',{'messages': messages.get_messages(request)})
        
        elif CustomUser.objects.filter(phone_number=phone_number).exists():
            messages.error(request, "phone number is al already exists"  )
            return render(request,'userside/signup.html',{'messages': messages.get_messages(request)})
        
        else:
            CustomUser.objects.create_user(username=email,first_name = first_name, email=email, phone_number=phone_number, password=password)
            send_6_digit_otp_email(request)
            return redirect('otp_verification')
    else:
        return render(request, 'userside/signup.html')    
    
    
    

def otp_verification(request): 
    
    expirationtime=request.session.get('otp_expiration_time')
    expire=datetime.strptime(expirationtime,"%Y-%m-%d %H:%M:%S")
    otp=request.POST.get('entered_otp')
    otp1=request.session.get('otp')
    email=request.session.get('recipient_email')
    user=CustomUser.objects.filter(email=email).first()

    if request.method=='POST':
        print('ddddddddddddddddddddddddddddddd')
        if (datetime.now()<=expire and otp==otp1):
            user.is_listed=True
            user.save()
            print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
            messages.success(request, 'user created successfully')
            return redirect('signup')
        elif(datetime.now()<=expire and otp != otp1):
            messages.error(request,'invalid otp')
            return redirect('otp_verification')
        else:
            messages.error(request,'time expired')
            return redirect('otp_verification')

    
    return render(request,'userside/otp_verification.html',{'expiration_time': expirationtime, 'expire':expire})

    
