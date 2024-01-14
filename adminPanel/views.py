from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib import messages
from userAuthentication.models import *
from products.models import *
from django.contrib.auth import authenticate,login, logout as auth_logout
from django.views.decorators.cache import cache_control
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import user_passes_test
from order.models import OrdersItem
from django.http import JsonResponse






# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminlogin(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('usertable')

    if request.method == 'POST':
        adminuser = request.POST.get('username')
        password = request.POST.get('password')

        useradmin = authenticate(username=adminuser,password=password)
        
        if useradmin is not None and useradmin.is_superuser:
            login(request,useradmin)
            return redirect('usertable')
        else:
            messages.error(request, "password or username is invalid")
            return render(request, 'adminside/adminlogin.html')
  
    return render(request, 'adminside/adminlogin.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="adminlogin")
def logoutadmin(request):
    if request.user:
        auth_logout(request)
    return redirect('adminlogin')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="adminlogin")
def usertable(request):
    if request.user.is_superuser:
        users = CustomUser.objects.exclude(is_superuser=True).all()
        context = {
            "users": users
        }
        return render(request, 'adminside/usertable.html',context)
    else:
        return redirect('adminlogin')
    

    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="adminlogin")
def addproduct(request):
    cat=Category.objects.all()
    bran=Brands.objects.all()
    if request.method == 'POST':
        product = request.POST.get('product_name')
        price = request.POST.get ('price')
        stock = request.POST.get('stock')
        category=request.POST.get('category')
        brand=request.POST.get('brand')
        image = request.FILES.getlist('product_image')
        c=Category.objects.filter(id=category).first()
        b=Brands.objects.filter(id=brand).first()
        products = Products(products_name=product, category_id=c,brand_id=b, price=price, stock=stock)
        products.save()
        for i in image:
            images = Image(product_id=products,image=i)
            images.save()
        return redirect('producttable')
    context={
        'cat':cat,
        'bran':bran
    }
    return render(request,'adminside/addproduct.html',context)
    


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="adminlogin")
def editproduct(request,id):
    cat=Category.objects.all()
    bran=Brands.objects.all()
    prod=Products.objects.filter(id=id).first()

    if request.method == 'POST':  
        product = request.POST.get('product_name')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        category = request.POST.get('category')
        brand=request.POST.get('brand')
        image = request.FILES.getlist('product_image')
        c=Category.objects.filter(id=category).first()
        b=Brands.objects.filter(id=brand).first()
        products = Products(id=id,products_name=product, category_id=c,brand_id=b, price=price, stock=stock)
        products.save()
        if image:
            for i in image:
                images = Image(product_id=products,image=i)
                images.save()
        return redirect('producttable')
    context={
        'cat':cat,
        'bran':bran,
        'prod':prod
    }
    return render(request,'adminside/editproduct.html',context)

def delete_images(request):
    if request.method == 'POST':
        print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        image_ids = request.POST.getlist("image_ids[]")
        print('bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb') 

        print(image_ids) 
        try:
            image_ids = list(map(int, image_ids))  # Convert strings to integers
            for image_id in image_ids:
                 print(type(image_id))

            print('cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc')
            # Delete images based on the received IDs
            images_to_delete = Image.objects.filter(pk__in=image_ids)
            print('ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd')
            print(images_to_delete)
            for image in images_to_delete:
                image.delete()
                print('eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')

            return JsonResponse({'message': 'Images deleted successfully'}, status=200)

        except Exception as e:
            return JsonResponse({'message': 'Error deleting images', 'error': str(e)}, status=500)
    
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="adminlogin")    
def producttable(request):
    if request.user.is_superuser:
        products = Products.objects.all()
        context = {
            "products":products
        }
        return render(request,'adminside/producttable.html',context)
    else:
        return render(request,'adminside/adminlogin.html')
    


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="adminlogin")
def categorytable(request):
    if request.user:
        categories = Category.objects.all()
        context = {
            "categories":categories
        }
        return render(request,'adminside/categorytable.html',context)    
    else:
        return render(request,'adminside/adminlogin.html')
    


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="adminlogin")
def brandtable(request):
    brands = Brands.objects.all()
    context = {
        'brands': brands
    }
    return render(request, 'adminside/brandtable.html',context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="adminlogin")
def deleteproduct(request,id):
    if request.method == 'POST':
        products = Products.objects.get(id=id)
        products.delete()
        return redirect('producttable')
    else:
        return render(request,'adminside/producttable.html')
    


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="adminlogin")
def product_status(request,id):
    product = Products.objects.filter(id=id).first()
    if product.is_listed == True:
        product.is_listed = False
        product.save()

    else:
        product.is_listed = True
        product.save()
    return redirect('producttable') 
 

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="adminlogin")
def user_status(request,id):
    user = CustomUser.objects.filter(id=id).first()
    if user.is_listed == True:
        user.is_listed = False
        user.save()
    else:
        user.is_listed = True
        user.save()
    return redirect('usertable')     

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="adminlogin")
def addcategory(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        id = request.POST.get('category_id')
        category_name = request.POST.get('category_name')

        if Category.objects.filter(name__iexact=category_name).exists():
            messages.error(request,'category already exists')
            return redirect('addcategory')
        else:
            category = Category(id=id, name=category_name)
            category.save()
            return redirect('categorytable')
    else:
        return render(request,'adminside/addcategory.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="adminlogin")
def editcategory(request,id):
    category = Category.objects.filter(id=id).first()
    if request.method == 'POST':
        category_name= request.POST.get('category_name') 
        category.name = category_name
        category.save()
        return redirect('categorytable')
    else:
        context={
               'category':category
        }
        return render(request,'adminside/editcategory.html',context)
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="adminlogin")
def deletecategory(request,id):
    if request.method == 'POST':
        category = Category.objects.get(id=id)
        category.delete()
        return redirect('categorytable')
    else:
        return render(request,'adminside/categorytable.html')
    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="adminlogin")
def category_status(request,id):
    category = Category.objects.filter(id=id).first()
    if category.is_listed == True:
        category.is_listed = False
        category.save()
    else:
        category.is_listed = True
        category.save()
    return redirect('categorytable')  


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="adminlogin")
def addbrand(request):
    if request.method == 'POST':
        id = request.POST.get('brand_id')
        brand_name = request.POST.get('brand_name')
        if Brands.objects.filter(name__iexact=brand_name).exists():
            messages.error(request,'This brand already exists')
            return redirect('addbrand')
        else:
            brand = Brands(id=id, name=brand_name)
            brand.save()
            return redirect('brandtable')
    else:
        return render(request,'adminside/addbrand.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="adminlogin")
def editbrand(request,id):
    brand = Brands.objects.filter(id=id).first()
    if request.method == 'POST':
        brand_name= request.POST.get('brand_name') 
        brand.name = brand_name
        brand.save()
        return redirect('brandtable')
    else:
        context={
                'brand':brand
        }
        return render(request,'adminside/editbrand.html',context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="adminlogin")  
def deletebrand(request,id):
    if request.method == 'POST':
        brand = Brands.objects.filter(id=id)
        brand.delete()
        return redirect('brandtable')
    else:
        return render(request,'adminside/brandtable.html')   
    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="adminlogin")
def brand_status(request,id):
    brands = Brands.objects.filter(id=id).first()
    if brands.is_listed == True:
        brands.is_listed = False
        brands.save()
    else:
        brands.is_listed = True
        brands.save()
    return redirect('brandtable')      


#orders 

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="adminlogin")
def orders(request):
    order_items = OrdersItem.objects.all().order_by("-id")
    return render(request,'adminside/orders.html',{"orders":order_items})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="adminlogin")
def order_details(request,id):
    order= OrdersItem.objects.filter(id=id).first()
    if request.method == 'POST':
         option = request.POST.get('options')
         if option:
            order.status = option
            order.save()

    statuses=['Order confirmed','Cancelled','Delivered']
    return render(request,'adminside/order_details.html',{'order':order, 'statuses':statuses})



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="adminlogin")

def reports(request):
    return render(request,'adminside/reports.html')


