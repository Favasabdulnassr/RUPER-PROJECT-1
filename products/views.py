from django.shortcuts import render,redirect
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import user_passes_test
from products.models import Products    
from django.contrib import messages

# Create your views here.


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="adminlogin")
def product_offers(request):
    products = Products.objects.filter(product_offer__gt=0)
    return render(request,'adminside/product_offer.html',{'products':products})





@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="adminlogin")
def add_product_offers(request):
    products = Products.objects.all().order_by("id")
    
    if request.method == "POST":
        
        product_name = request.POST.get("product")

        if not product_name:
            messages.error(request,"please select a product")
            return render(request, 'adminside/add_product_offers.html', {"products": products})

        product_discount = request.POST.get("discount")

        if int(product_discount) > 99 or int(product_discount) == 0:
            messages.error(request,"dicount percentage should be between 1 and 100")
            return render(request, 'adminside/add_product_offers.html', {"products": products})

     
        product = Products.objects.get(id=product_name)
        product.product_offer = product_discount
        product.save()
        return redirect("product_offers")
    
    return render(request,'adminside/add_product_offers.html',{"products":products})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="adminlogin")
def edit_product_offer(request,id):
    products = Products.objects.all().order_by("id")
    item = Products.objects.get(id=id)

    if request.method == "POST":
        product_discount = request.POST.get("discount")
        
        if int(product_discount) > 99 or int(product_discount) == 0:
            messages.error(request,"dicount percentage should be between 1 and 100")
            return render(request, 'adminside/edit_product_offers.html', {"products": products})

        item.product_offer = product_discount
        item.save()
        return redirect("product_offers")
    return render(request,'adminside/edit_product_offers.html',{'item':item,'products':products})




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="adminlogin")
def cancel_product_offer(request,id):
    item = Products.objects.get(id=id)
    item.product_offer = 0
    item.save()
    return redirect('product_offers')
 
 