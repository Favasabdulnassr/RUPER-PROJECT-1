from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib import messages
from userAuthentication.models import *
from django.contrib.auth import authenticate,login as auth_login, logout as auth_logout
from django.views.decorators.cache import cache_control
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import user_passes_test


# Create your views here.
@never_cache
def adminlogin(request):
    if request.user.is_superuser:
        return redirect('usertable')

    if request.method == 'POST':
        adminuser = request.POST['username']
        password = request.POST['password']

        useradmin = authenticate(username=adminuser,password=password)
        
        if useradmin is not None and useradmin.is_superuser:
            auth_login(request,useradmin)
            return redirect('usertable')
        else:
            messages.error(request, "password or username is invalid")
            return redirect('adminlogin')
  
    return render(request, 'adminside/adminlogin.html')

@never_cache
def logoutadmin(request):
    if request.user:
        auth_logout(request)
    return redirect('adminlogin')


def usertable(request):
    if request.user.is_superuser:
        users = CustomUser.objects.exclude(is_superuser=True).all()
        context = {
            "users": users
        }
        return render(request, 'adminside/usertable.html',context)
    else:
        return redirect('adminlogin')
    
@never_cache
def productable(request):
    if request.user.is_superuser:
        return redirect('productable')
    else:
        return render(request,'adminside/adminlogin.html')
    
def categorytable(request):
    return render(request,'adminside/categorytable.html')    

def brandtable(request):
    return render(request, 'adminside/brandtable.html')
