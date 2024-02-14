from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from .models import Cart
from products.models import Products
from decimal import Decimal
from userAuthentication.models import CustomUser
from userprofile.models import Address
from django.contrib import messages
from coupon.models import Coupons, CouponUsage
from django.utils import timezone
from datetime import timedelta, datetime


def add_cart(request):
    if request.method == 'POST':
        quantity = request.POST.get('quantity', 1)
        id = request.POST.get("id") 
        product = Products.objects.get(id = id)

        
        if product.stock >= quantity:
            if Cart.objects.filter(customuser=request.user, product=product).exists():
                return JsonResponse({'success': False})  
            
            # Create or update cart for the user
            cart, created = Cart.objects.get_or_create(
                customuser=request.user, product=product
            )
            price = product.discounted_price()
            cart.quantity = quantity
            cart.cart_price = price * Decimal(quantity)
            cart.save()

            response_data = {
                'success': True,
                'message': 'Item added to cart successfully.'
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({'success': False, 'message': 'Product out of stock'})

    return JsonResponse({'success': False})

def remove_item_cart(request):  
    if request.method == "POST":
        item_id = request.POST.get('item_id')
        try:
            cart_item = Cart.objects.get(id=item_id)
            cart_item.delete()
            return JsonResponse({"message":"item removed successfully"})
        except Cart.DoesNotExist:
            return JsonResponse({"message": "item not found"}, status=400)
        
    else:
        return JsonResponse({"message": "Invalid request method"}, status=405)     
    


def update_cart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user
            userr = CustomUser.objects.filter(email=user.email).first()
            change = int(request.POST.get('change'))
            cart_id = int(request.POST.get('productId'))
            cart = Cart.objects.get(id=cart_id)
            
            product_obj = Products.objects.get(id=cart.product.id)

            if change == 1:
                if product_obj.stock > cart.quantity:
                    cart.quantity += 1
                    cart.save()
            else:
                if cart.quantity > 1:
                    cart.quantity -= 1
                    cart.save()
                else:
                    cart.quantity = 1
                    cart.save()    

            prodTotal = product_obj.discounted_price() * cart.quantity
            cart.cart_price = prodTotal
            cart.save()     
            cart_items = Cart.objects.filter(customuser=userr)
            total = sum(cart_items.values_list('cart_price',flat=True))
           

            responsData = {
                'updatedQuantity':cart.quantity,
                'prodTotal':prodTotal,
                'totalCartPrice':total
            }
            return JsonResponse(responsData)

    return HttpResponse(status=200)




def cart(request):
    user = request.user
    cart_item = Cart.objects.filter(customuser=user)
    total = sum(cart_item.values_list('cart_price',flat=True))
    context ={
        'cart_item': cart_item,
        'total': total
    }

    return render(request,'userside/cart.html',context)


def checkout(request):
    if request.user.is_authenticated:
        user = request.user
        cart_item = Cart.objects.filter(customuser=user)
        if cart_item.exists():

            userr = request.user
            user = CustomUser.objects.filter(email=userr.email).first()
            address = Address.objects.filter(user=user)
            cart_items = Cart.objects.filter(customuser=user)
            total = sum(cart_items.values_list('cart_price',flat=True))
            coupons = Coupons.objects.filter(is_active=True).filter(expiration_date__gte=timezone.now())
            context = {
                'coupons':coupons,
                'addresses': address,
                'cart_items': cart_items,
                'total': total
            }
            return render(request, 'userside/checkout.html',context)
        else:
            return redirect('cart')
    else:
        return redirect ('signin')


def edit_address(request,id):
    if request.method == 'POST':
        user_address = Address.objects.filter(id=id).first()
        user_address.name = request.POST.get('name')
        user_address.phone = request.POST.get('phone')
        user_address.street_address = request.POST.get('street_address')
        user_address.city = request.POST.get('city')
        user_address.state = request.POST.get('state')
        user_address.pin_code = request.POST.get('pincode')

        user_address.save()
        return redirect('checkout')
        

    user_address = Address.objects.filter(id=id).first()
    return render(request,'userprofile/editAddress.html',{'user_data':user_address})


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
        return redirect('checkout')
    
    return render(request,'userprofile/addaddress.html')

def apply_coupon(request):
    if request.method == 'POST':
        email = request.user.email
        user = CustomUser.objects.get(email=email)

        coupon_code = request.POST.get('couponCode')
        coupon_check = Coupons.objects.filter(code=coupon_code ,is_active=True).first()
        if coupon_check:
            if CouponUsage.objects.filter(user=user,coupon=coupon_check).exists():
                return JsonResponse({"error": "Coupon already applied"})
            else:
                if coupon_check.used_count < coupon_check.usage_limit:
                    cart_total = sum(Cart.objects.filter(customuser=user).values_list("cart_price",flat=True))

                    if cart_total >= coupon_check.minimum_purchase:
                        if coupon_check.expiration_date < datetime.now().date():
                            return JsonResponse({"error":"coupon expired"})
                        
                        total = cart_total - coupon_check.discount_value
                        request.session['final_amount'] = int(total)
                        request.session['coupon_Code']  = coupon_code

                        response_data = {
                            "success":"added",
                            "total" : total,
                            "coupon_code" : coupon_code,
                            "discount_amount" : coupon_check.discount_value

                        }
                        coupon_check.used_count +=1
                        coupon_check.save()

                        CouponUsage.objects.create(user=user,coupon = coupon_check)

                        return JsonResponse(response_data)
                    
                    else:
                        return JsonResponse({"error": f"Minimum purchase amount of {round(coupon_check.minimum_purchase)} required"})
                    
                else:

                    return JsonResponse({"error":"This code has reached this maximum limit"})
        else:
            return JsonResponse({"error":"invalid coupon"})
    else:
        return JsonResponse({"error":"invalid request"})       
    

def remove_coupon(request):    
    email = request.user.email
    user = CustomUser.objects.get(email=email)

    coupon_code = request.POST.get("couponCode")
    coupon_check = Coupons.objects.filter(code=coupon_code,is_active=True).first()
    if coupon_check:
            usage_check = CouponUsage.objects.filter(user=user,coupon=coupon_check).first()
            print(usage_check.ordered)
            if usage_check:
                if usage_check.ordered == 1:
                    return JsonResponse({"error":"This Coupon is already applied"})
                else:
                    coupon_check.used_count -= 1
                    coupon_check.save()
                    usage_check.delete()
    total = sum(Cart.objects.filter(customuser=user).values_list('cart_price',flat=True))   
    if 'final_amount' in request.session:
        del request.session['final_amount']
        
    response_data= ({"success":"removed",'total':total})
    
    return JsonResponse(response_data)    

