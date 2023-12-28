from django.shortcuts import render,redirect
from products.models import *


# Create your views here.
def Home(request):
    return render(request,'userside/home.html')


def shop(request):
    cat=request.GET.get('categoryy','0')
    if cat != '0':
        products = Products.objects.filter(category_id__id=cat).all()
    else:
        products = Products.objects.all()

    categories = Category.objects.all()

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

def checkout(request):
    return render(request, 'userside/checkout.html')

def shopdetails(request,id):
    products = Products.objects.filter(id=id).first()
    context ={
        'products':products
    }
    return render(request, 'userside/shopdetails.html',context)
