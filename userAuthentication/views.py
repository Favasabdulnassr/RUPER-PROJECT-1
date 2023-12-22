from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login, logout as auth_logout
from userAuthentication.models import CustomUser
from products.models import *

# Create your views here.




def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        return redirect('home')
    else:
        return render(request,'userside/home.html')

def login(request):
    if request.user.is_authenticated:
        return render(request,'userside/home.html')
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
               


def signup(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        email = request.POST.get('email1')
        phone_number = request.POST.get('phone1')
        password = request.POST.get('password1')
    
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "email is already exists")
            print('email error')
            return render(request,'userside/signup.html',{'messages': messages.get_messages(request)})
        
        elif CustomUser.objects.filter(phone_number=phone_number).exists():
            messages.error(request, "phone number is al already exists"  )
            return render(request,'userside/signup.html',{'messages': messages.get_messages(request)})
        
        else:
            user = CustomUser.objects.create_user(username=email,first_name=first_name,email=email, phone_number=phone_number, password=password)
            messages.info(request, "User created successfully")
            print('sucess')
            return redirect('otp_verification', username=email)
    else:
        return render(request, 'userside/signup.html')    
    

def otp_verification(request, username):
    if request.method == "POST":
        entered_otp = request.POST.get('entered_otp')
        

        user = CustomUser.objects.get(username=username)
        print(entered_otp)
        print(user.email_otp)
        if entered_otp == user.email_otp:  # Assuming the user has been retrieved by username
            user.email_verified = True
            user.save()
            messages.success(request, "Email verified successfully. You can now log in.")
            return redirect('signup')  # Redirect to login page or any other page

        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return render(request, 'userside/otp_verification.html')

    else:
        return render(request, 'userside/otp_verification.html')
    
