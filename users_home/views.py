from django.shortcuts import render,redirect
from products.models import *
from userAuthentication.models import CustomUser
from userprofile.models import Address
from cart.models import Cart
from products.models import Products,Category
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from adminPanel.models import Banner


# Create your views here.
def Home(request):
    product = Products.objects.all().order_by("pk")
    banner = Banner.objects.all().order_by("pk")

    first_product = product[0]
    first_product_image = first_product.image_set.all()
    first_image =  first_product_image[0]

    second_product = product[1]
    second_product_image = second_product.image_set.all()
    second_image = second_product_image[0]

    third_product = product[2]
    third_product_image = third_product.image_set.all()
    third_image = third_product_image[0]

    all_images = Image.objects.filter(product_id__in=product).order_by("-id")



    return render(request,'userside/home.html',{
        'products': product,
        'first_image':first_image,
        'second_image':second_image,
        'all_images' : all_images,
        'banner':banner,
        'third_image':third_image,
       
    })

def search(request):
    search = request.GET.get('search', '')
    cat = request.GET.get('categoryy', '0')
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
