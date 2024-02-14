from django.shortcuts import render,redirect
from userAuthentication.models import CustomUser
from cart.models import Cart
from django.http import JsonResponse
from userprofile.models import Address
from django.db import transaction
from.models import *
from datetime import timedelta
from django.contrib import messages
from django.core.cache import cache
from coupon.models import CouponUsage, Coupons
from wallet.models  import Wallet
# from django.contrib.auth.decorators import login_required
# from django.views.decorators.cache import never_cache
# Create your views here.




def order_successfull(request):
    if request.user.is_authenticated:
        order_id = request.session['order_id']
        current_order = Orders.objects.get(order_id=order_id)
        return render(request,'userside/order_successfull.html',{'orders': current_order})
    
def cancel_order(request,id):
    email = request.user.email
    user = CustomUser.objects.get(email=email)
    order = OrdersItem.objects.get(id=id)
    if order.status != 'Delivered':
        order.status = "Cancelled"

        if order.order.payment_method == 'cod':
            order.product.stock += order.quantity
            order.save()
            order.product.save()
            if request.user == request.user.is_superuser:
                return redirect('orders') 
            else:
                return redirect('myaccount')
        else:
            order.product.stock += order.quantity
            amount = order.price*order.quantity

            user_wallet = Wallet.objects.filter(user=user).order_by('-id').first()

            if user_wallet:
                balance = user_wallet.balance
            else:
                balance = 0

            new_balance = amount + balance

            Wallet.objects.create(
                user = user,
                amount = amount,
                balance = new_balance,
                transaction_type = "Credit",
                transaction_details = "Received money by cancel order",
            )       

            order.save()
            order.product.save() 

            if request.user == request.user.is_superuser:
                return redirect('orders') 
            else:
                return redirect('myaccount')

    else:
        messages.error(request,'product already delivered ')  
        return redirect('orderss') 


def placer_order(request):
    if request.user.is_authenticated:
        email = request.user.email
        user_instance = CustomUser.objects.get(email=email)


        cart_items = Cart.objects.filter(customuser=user_instance)
        out_of_stock_items = [item for item in cart_items if item.quantity > item.product.stock]
        if out_of_stock_items:
            return JsonResponse({'empty': True, 'message': 'Some cart items are out of stock'})
# function for placing order        
        if request.method == 'POST':
            address_id = request.POST.get('address')
            payment_type = request.POST.get('payment')
            cart_items = Cart.objects.filter(customuser=user_instance)
            delivery_address = Address.objects.filter(id=address_id).first()
            
            if cart_items.exists():
                try:
                    with transaction.atomic():
                        if 'final_amount' in request.session:
                            final_amount = int(request.session['final_amount'])
                            
                            coupon_code = request.session['coupon_Code']
                            coupon_check = Coupons.objects.filter(code=coupon_code,is_active=True).first()
                            user= request.user
                            coupon_used = CouponUsage.objects.filter(user=user,coupon=coupon_check).first()
                            coupon_used.ordered = 1
                            coupon_used.save()
                        else: 
                            total_amount = sum(cart_item.product.price*cart_item.quantity for cart_item in cart_items)

# Create a new order instance
                        order = Orders.objects.create(
                            user = user_instance,
                            address = delivery_address,
                            payment_method = payment_type,
                            quantity = 0,
                            total_purchase_amount = final_amount if 'final_amount' in request.session else total_amount
                        )       

                        for cart_item in cart_items:
# Create an order item for each cart item
                            order_item = OrdersItem.objects.create(
                                order = order,
                                product = cart_item.product,
                                quantity = cart_item.quantity,
                                price = cart_item.product.price,
                                total_item_amount = cart_item.cart_price,
                                status = 'Order confirmed',
                            )

# for decrementing quantity
                            products = cart_item.product
                            products.stock -= cart_item.quantity
                            products.save()
# Update the order's quantity
                            order.quantity += order_item.quantity
# delete cart_item from cart
                            cart_item.delete()

# calculate the expected delivery date
                        order.expected_delivery_date =  (order.order_date + timedelta(days=7))
                        order.save()
                        request.session['order_id'] = str(order.order_id)

                        if payment_type == "Wallet":
                            email = request.user.email
                            user = CustomUser.objects.get(email=email)

                            user_wallet = Wallet.objects.filter(user=user).order_by('-id').first()
                            total_amount = final_amount if 'final_amount' in request.session else total_amount

                            if user_wallet:
                                balance = user_wallet.balance
                            else:
                                balance = 0

                            new_balance = balance - total_amount      

                            Wallet.objects.create(
                                user = user,
                                amount = total_amount,
                                balance = new_balance,
                                transaction_type = 'Debit',
                                transaction_details = "Debit money by place order"
                            ) 
                            
                            

                        respone_data = {
                            'success': True,
                            'message': 'Order placed successfully',
                            'order_id': order.order_id,
                        }
                        return JsonResponse(respone_data)

                except Exception as e:
                    response_data = {
                        'success' : False,
                        'message' : 'errore while placing the order'
                    }     

                    return JsonResponse(response_data)                                  

            else:
                response_data={
                    'success': False,
                    'message': 'your cart is empty',
                }     
                return JsonResponse(respone_data)
        else:
            response_data={
                'success': False,
                'message': 'user not logged in'
            }
            return JsonResponse(response_data)
        
def proceed_to_pay(request):
    user = request.user
    cart = Cart.objects.filter(customuser=user)
    total_price = 0
    for item in cart:
        total_price += item.cart_price
    name = user.first_name
    email = user.email    
    contact = user.phone_number
    return JsonResponse({'total_price':total_price, 'email':email, 'name':name, 'contact':contact})     

def view_invoice(request):
    order_id = request.session["order_id"]
    current_order = Orders.objects.get(order_id=order_id)
    context = {"current_order":current_order}
    return render(request,"userside/invoice.html",context)


