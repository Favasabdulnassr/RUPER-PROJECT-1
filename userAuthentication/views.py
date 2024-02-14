from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login, logout as auth_logout
from userAuthentication.models import CustomUser
from products.models import *
import random
from datetime import datetime, timedelta
from django.core.mail import send_mail
from wallet.models import Wallet

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
            return redirect('home')
        
        else:
            messages.error(request, "invalid password or username") 
            return redirect('home')
          
    else:
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
        phone_number = request.POST.get('phone1'),
        password = request.POST.get('password1')
        request.session['recipient_email'] = email
        refferal_id = request.POST.get('referral_id')
        reffered_user = None
        if refferal_id:
            reffered_user = CustomUser.objects.filter(referal_id=refferal_id).first()
            if reffered_user is None:
               messages.error(request,'Invalid referal Id')
               return render(request,'userside/signup.html',{'messages': messages.get_messages(request)})
            else:
              pass
        else:
            pass        
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "email is already exists")
            return render(request,'userside/signup.html',{'messages': messages.get_messages(request)})
        
        elif CustomUser.objects.filter(phone_number=phone_number).exists():
            messages.error(request, "phone number is al already exists"  )
            return render(request,'userside/signup.html',{'messages': messages.get_messages(request)})
        
        else:
            if reffered_user:
                CustomUser.objects.create_user(username=email,first_name = first_name, email=email, phone_number=phone_number, password=password,reffered=1,reffered_id=refferal_id )
                send_6_digit_otp_email(request)
                return redirect('otp_verification')
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
        if (datetime.now()<=expire and otp==otp1):
            user.is_listed=True
            if user.reffered == 1:
                Wallet.objects.create(
                    user = user,
                    amount = 100,
                    balance = 100,
                    transaction_type = 'Credit',
                    transaction_details = "Added money by created account using refferal",

                )

                reffered_id = user.reffered_id
                reffered_usssser = CustomUser.objects.get(referal_id=reffered_id)
                reffered_user = Wallet.objects.filter(user=reffered_usssser).order_by("-id").first()

                if reffered_user:
                    balance = reffered_user.balance
                else:
                    balance = 0

                new_balance = balance + 100

                Wallet.objects.create(
                user = reffered_usssser,
                amount = 100,
                balance = new_balance,
                transaction_type = 'Credit',
                transaction_details = "Added money by user created by your refferal",

                )


                


            user.save()

            messages.success(request, 'user created successfully')
            return redirect('home')
        
        elif(datetime.now()<=expire and otp != otp1):
            messages.error(request,'invalid otp')
            return redirect('otp_verification')
        else:
            messages.error(request,'time expired')
            return redirect('otp_verification')

    
    return render(request,'userside/otp_verification.html',{'expiration_time': expirationtime, 'expire':expire})

    