from django.shortcuts import render,redirect
from userAuthentication.models import CustomUser
from cart.models import Cart
from django.http import JsonResponse
from userprofile.models import Address
from django.db import transaction
from.models import *
from datetime import timedelta
from django.contrib import messages
# Create your views here.




def order_successfull(request):
    if request.user.is_authenticated:
        order_id = request.session['order_id']
        print('ssssssssss',order_id)
        current_order = Orders.objects.get(order_id=order_id)

        return render(request,'userside/order_successfull.html',{'orders': current_order})
    
def cancel_order(request,id):
    order = OrdersItem.objects.get(id=id)
    if order.status != 'Delivered':
        order.status = "Cancelled"
        order.product.stock += order.quantity
        order.save()
        order.product.save()
        return redirect('orderss') 
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
                        if 'total' in request.session:
                            total_amount = int(request.session['total'])
                        else:
                            total_amount = sum(cart_item.product.price*cart_item.quantity for cart_item in cart_items)

  # Create a new order instance
                        order = Orders.objects.create(
                            user = user_instance,
                            address = delivery_address,
                            payment_method = payment_type,
                            quantity = 0,
                            total_purchase_amount = total_amount
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

                        respone_data = {
                            'success': True,
                            'message': 'Order placed successfully',
                            'order_id': order.order_id,
                        }
                        return JsonResponse(respone_data)

                except Exception as e:
                    print(f"error while placing the order: {e}") 
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
        


