from django.shortcuts import render,redirect
from userAuthentication.models import CustomUser
from userprofile.models import Address
from cart.models import Cart
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
import re
from django.http import JsonResponse
from order.models import OrdersItem,Orders
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
@login_required
def myaccount(request):
    user = request.user
    user_data = Address.objects.filter(user=user)
    orders = Orders.objects.filter(user=user)
    order_items = OrdersItem.objects.filter(order__in=orders).order_by("-id")
 

    return render(request, 'userprofile/myaccount.html', {"address_data": user_data, "order_items": order_items})



def update_account(request):
    if request.method == 'POST':
        email = request.user.email
        user = CustomUser.objects.get(email=email)

        first_name = request.POST.get("account_first_name")
        if not re.match(r"^[a-zA-Z]{3,}(?: [a-zA-Z]+)*$", first_name):
            messages.error(request, "Invalid full name.")
            return redirect("myaccount")
        
        last_name = request.POST.get("account_last_name")
        if not re.match(r"^[a-zA-Z]{3,}(?: [a-zA-Z]+)*$",last_name ):
            messages.error(request, "Invalid full name.")
            return redirect("myaccount")
        

        new_phone = request.POST.get("new_phone_number")
        if not re.match(r"^[1-9][0-9]{9}$", new_phone):
            messages.error(
                request,
                "Invalid phone number. Please enter a valid Indian phone number.",
            )
            return redirect("myaccount")
        if CustomUser.objects.exclude(id=user.id).filter(phone_number=new_phone).exists():
            messages.error(request, "Phone number already exists in the database.")
            return redirect("myaccount")
        
        user.first_name = first_name
        user.last_name = last_name
        user.phone_number = new_phone
        user.save()
        messages.success(request,"updated successfully")
        
    return redirect("myaccount")


# change password

def change_password(request):
    if request.method == 'POST':
        user = request.user
        current_password = request.POST.get("password_current")
        new_password = request.POST.get("new_password_1")
        confirm_password = request.POST.get("new_password_2")

        user_new = authenticate(username=request.user.email, password=current_password)

        if user_new == user:
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                return redirect('myaccount')
            else:
                messages.error(request,'passwords do not match')
                return redirect('myaccount')
        else:
            messages.error(request,'current password is not correct')
            return redirect('myaccount') 
           
    return redirect('myaccount')

def edit_address(request,id):
    if request.method == 'POST':
        user_address = Address.objects.filter(id=id).first()
        user_address.name = request.POST.get('name')
        user_address.phobe = request.POST.get('phone')
        user_address.street_address = request.POST.get('street_address')
        user_address.city = request.POST.get('city')
        user_address.state = request.POST.get('state')
        user_address.pin_code = request.POST.get('pincode')

        user_address.save()
        return redirect('myaccount')
        

    user_address = Address.objects.filter(id=id).first()
    return render(request,'userprofile/editaddress.html',{'user_data':user_address})


def add_address(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        street_address= request.POST.get('street_address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')

        Address.objects.create(user=request.user,name=name, phone=phone, street_address= street_address, city=city, state=state, pin_code=pincode)
        messages.info(request,'Address created successfully')
        return redirect('myaccount')
    
        
    return render(request,'userprofile/addaddress.html')

def delete_address(request,id):
    user_address = Address.objects.filter(id=id).first()
    if user_address:
        user_address.delete()
        return JsonResponse({'message': 'Address deleted successfully.'})
    else:
        return JsonResponse({'message': 'Address not found.'}, status=404)


    