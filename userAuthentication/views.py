from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login, logout as auth_logout
from userAuthentication.models import CustomUser
from products.models import *

# Create your views here.


def Home(request):
    if request.user.is_authenticated:
        return render(request, 'userside/home1.html')
    return render(request,'userside/home.html')

def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        return redirect('home')
    else:
        return render(request,'userside/home1.html')

def login(request):
    if request.user.is_authenticated:
        return render(request,'userside/home1.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request,user)
            return redirect('home1')
        
        else:
            messages.error(request, "invalid password or username") 
            return render(request, "userside/home.html") 
    else:
        return render(request, "userside/home.html")          

def Home1(request):
    if request.user.is_authenticated:
        return render(request,'userside/home1.html')
    else:
        return redirect('home')

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username1')
        email = request.POST.get('email1')
        phone_number = request.POST.get('phone1')
        password = request.POST.get('password1')
    
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'username already exists')
            print('username already exists')
            return render(request,'userside/signup.html',{'messages': messages.get_messages(request)})
        
        
        elif CustomUser.objects.filter(email=email).exists():
            messages.error(request, "email is already exists")
            print('email error')
            return render(request,'userside/signup.html',{'messages': messages.get_messages(request)})
        
        elif CustomUser.objects.filter(phone_number=phone_number).exists():
            messages.error(request, "phone number is al already exists"  )
            return render(request,'userside/signup.html',{'messages': messages.get_messages(request)})
        
        else:
            user = CustomUser.objects.create_user(username=username, email=email, phone_number=phone_number, password=password)
            messages.info(request, "User created successfully")
            print('sucess')
            return redirect('otp_verification', username=username)
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
    
def shop(request):
    products = Products.objects.all()
    categories = Category.objects.all()
    # for category in categories:
    #     category.item_count = category.count()
    brands = Brands.objects.all()

    context = {
             'products': products,
             'categories' : categories,
             'brand' : brands
    }
    return render(request,'userside/shop.html',context)

def contact(request):
    return render(request,'userside/contact.html')    

def myaccount(request):
    return render(request,'userside/myaccount.html')

def aboutus(request):
    return render(request, 'userside/aboutus.html')

def wishlist(request):
    return render(request, 'userside/wishlist.html')

def cart(request):
    return render(request, 'userside/cart.html')

def checkout(request):
    return render(request, 'userside/checkout.html')

def shopdetails(request):
    return render(request, 'userside/shopdetails.html')