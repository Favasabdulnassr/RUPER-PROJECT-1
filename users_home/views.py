from django.shortcuts import render,redirect
from products.models import *
from userAuthentication.models import CustomUser
from userprofile.models import Address
from cart.models import Cart
from products.models import Products,Category
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404


# Create your views here.
def Home(request):
    return render(request,'userside/home.html')

def search(request):
    search = request.GET.get('search', '')
    cat = request.GET.get('categoryy', '0')
    sort = request.GET.get('sort')
    cat_name=''

    if cat != '0':
        products = Products.objects.filter(is_listed=True,category_id__id=cat).order_by('-id')
        

    elif sort == 'price_low_to_high':
        products = Products.objects.filter(is_listed=True).order_by('price')

    elif sort == 'price_high_to_low':
        products = Products.objects.filter(is_listed=True).order_by('-price')

    else:
        products = Products.objects.filter(is_listed=True).order_by('-id')

    categories = Category.objects.all()
    brands = Brands.objects.all()

    if search:
        products = Products.objects.filter(products_name__icontains=search).order_by('-id')

    paginator = Paginator(products,3)
    page_num = request.GET.get('page',1)
    paginated_products = paginator.get_page(page_num)




    context = {
        'products': paginated_products,
        'categories':categories,
        'brand':brands,
        'cat':cat,
        'sort':sort,
        'search': search
        
    }        


    return render(request,'userside/shop.html',context)


def shop(request):
    cat=request.GET.get('categoryy','0')
    sort = request.GET.get('sort')

    if cat != '0':
        products = Products.objects.filter(is_listed=True,category_id__id=cat).order_by('-id')

    elif sort == 'price_low_to_high':
        products = Products.objects.filter(is_listed=True).order_by('price') 

    elif sort == 'price_high_to_low':
        products = Products.objects.filter(is_listed=True).order_by('-price')

    else:
        products = Products.objects.filter(is_listed=True).order_by('-id')

    categories = Category.objects.all()

    brands = Brands.objects.all()
    
    paginator = Paginator(products,3)
    page_num = request.GET.get('page',1)
    paginated_products = paginator.get_page(page_num)


    context = {
             'products': paginated_products,
             'categories' : categories,
             'brand' : brands,
             'cat' : cat,
             'sort': sort
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
