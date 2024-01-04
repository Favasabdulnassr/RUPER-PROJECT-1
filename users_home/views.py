from django.shortcuts import render,redirect
from products.models import *
from userAuthentication.models import CustomUser
from userprofile.models import Address
from cart.models import Cart


# Create your views here.
def Home(request):
    return render(request,'userside/home.html')


def shop(request):
    cat=request.GET.get('categoryy','0')
    if cat != '0':
        products = Products.objects.filter(is_listed=True,category_id__id=cat).order_by('-id')
    else:
        products = Products.objects.filter(is_listed=True).order_by('-id')

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


def aboutus(request):
    return render(request, 'userside/aboutus.html')

def wishlist(request):
    return render(request, 'userside/wishlist.html')



def shopdetails(request,id):
    products = Products.objects.filter(id=id).first()
    context ={
        'products':products
    }
    return render(request, 'userside/shopdetails.html',context)
