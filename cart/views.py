from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse,HttpResponse
from .models import Cart
from products.models import Products
from decimal import Decimal
from userAuthentication.models import CustomUser

def add_cart(request):
    if request.method == 'POST':
        quantity = request.POST.get('quantity', 1)
        id = request.POST.get("id") 
        print(id)
        product = Products.objects.get(id = id)
        
        if Cart.objects.filter(customuser=request.user, product=product).exists():
            return JsonResponse({'success': False})  
        
        # Create or update cart for the user
        cart, created = Cart.objects.get_or_create(
            customuser=request.user, product=product
        )
        price = product.price
        cart.quantity = quantity
        cart.cart_price = price * Decimal(quantity)
        cart.save()

        response_data = {
            'success': True,
            'message': 'Item added to cart successfully.'
        }
        return JsonResponse(response_data)

    return JsonResponse({'success': False})

def remove_item_cart(request):  
    if request.method == "POST":
        print('pooooooooooooooooooooooooooooooooooooooooooooooooooooooost')
        item_id = request.POST.get('item_id')
        print(item_id)
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
        print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
        if request.user.is_authenticated:
            user = request.user
            print(user)
            userr = CustomUser.objects.filter(email=user).first()
            print(userr)
            change = int(request.POST.get('change'))
            print(change)
            cart_id = int(request.POST.get('productId'))
            cart = Cart.objects.get(id=cart_id)
            
            product_obj = Products.objects.get(id=cart.product.id)
            print('uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu')
            print(product_obj)
            print(cart)
            print('BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB')

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

            prodTotal = product_obj.price * cart.quantity
            cart.cart_price = prodTotal
            cart.save()     
            cart_items = Cart.objects.filter(customuser=userr)
            total = sum(cart_items.values_list('cart_price',flat=True))

            responsData = {
                'updatedQuantity':cart.quantity,
                'prodTotal':prodTotal,
                'totalCartPrice':total

            }
            print('CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC')
            return JsonResponse(responsData)
        print("Not enterred")

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


