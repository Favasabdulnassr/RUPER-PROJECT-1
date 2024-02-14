from django.shortcuts import render,redirect
from userAuthentication.models import CustomUser
from .models import Wallet
import razorpay
from django.http import JsonResponse

# Create your views here.

def wallet(request):
    email = request.user.email
    user = CustomUser.objects.get(email=email)
    wallet = Wallet.objects.filter(user=user).order_by('-id')
    if wallet:
        balance = wallet.first().balance    
    else:
        balance = 0    

    context = {'balance':balance, 'wallets':wallet}
    
    return render(request,'userside/wallet.html',context)

client = razorpay.Client(auth=("rzp_test_LWQdkfQTzRGUBJ","jXE2IxqDvYVgxJGCbPJM3k71"))


def add_to_wallet(request):
    amount = int(request.POST.get("amount"))* 100
    data = {"amount":amount,'currency':'INR'}
    payment = client.order.create(data=data)

    request.session["amount"] = amount/100

    context = {"success":True,"payment":payment,"payment_id":payment["id"],"amount":amount}

    return JsonResponse(context)


def update_wallet(request):
    email = request.user.email
    amount = request.session["amount"]
    user_name = CustomUser.objects.get(email=email)
    user = Wallet.objects.filter(user=user_name).order_by("-id").first()
    if user:
        balance = user.balance
    else:
        balance = 0   

    new_balance = balance + amount

    Wallet.objects.create(
        user = user_name,
        amount = amount,
        balance = new_balance,
        transaction_type = 'Credit',
        transaction_details = "Added money through razorpay"

    )

    return redirect('wallet')


