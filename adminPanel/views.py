from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib import messages
from userAuthentication.models import *
from products.models import *
from django.contrib.auth import authenticate,login, logout as auth_logout
from django.views.decorators.cache import cache_control
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import user_passes_test




# Create your views here.
@never_cache
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

@never_cache
def logoutadmin(request):
    if request.user:
        auth_logout(request)
    return redirect('adminlogin')

def usertable(request):
    if request.user.is_superuser:
        users = CustomUser.objects.exclude(is_superuser=True).all()
        context = {
            "users": users
        }
        return render(request, 'adminside/usertable.html',context)
    else:
        return redirect('adminlogin')
    
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
        products = Products(products_name=product, category_id=c,brand_id=b, price=price, quantity=stock)
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
        products = Products(id=id,products_name=product, category_id=c,brand_id=b, price=price, quantity=stock)
        products.save()
        if image:
            p=Image.objects.filter(product_id=id)
            p.delete()
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



    
    
@never_cache
def producttable(request):
    if request.user.is_superuser:
        products = Products.objects.all()
        context = {
            "products":products
        }
        return render(request,'adminside/producttable.html',context)
    else:
        return render(request,'adminside/adminlogin.html')
    
def categorytable(request):
    if request.user:
        categories = Category.objects.all()
        context = {
            "categories":categories
        }
        return render(request,'adminside/categorytable.html',context)    
    else:
        return render(request,'adminside/adminlogin.html')
    

def brandtable(request):
    brands = Brands.objects.all()
    context = {
        'brands': brands
    }
    return render(request, 'adminside/brandtable.html',context)

def deleteproduct(request,id):
    if request.method == 'POST':
        products = Products.objects.get(id=id)
        products.delete()
        return redirect('producttable')
    else:
        return render(request,'adminside/producttable.html')
    

def product_status(request,id):
    product = Products.objects.filter(id=id).first()
    if product.is_listed == True:
        product.is_listed = False
        product.save()

    else:
        product.is_listed = True
        product.save()
    return redirect('producttable')  

def user_status(request,id):
    user = CustomUser.objects.filter(id=id).first()
    if user.is_listed == True:
        user.is_listed = False
        user.save()
    else:
        user.is_listed = True
        user.save()
    return redirect('usertable')     

def addcategory(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        id = request.POST.get('category_id')
        category_name = request.POST.get('category_name')
        category = Category(id=id, name=category_name)
        category.save()
        return redirect('categorytable')
    else:
        return render(request,'adminside/addcategory.html')

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
    
def deletecategory(request,id):
    if request.method == 'POST':
        category = Category.objects.get(id=id)
        category.delete()
        return redirect('categorytable')
    else:
        return render(request,'adminside/categorytable.html')
    

def category_status(request,id):
    category = Category.objects.filter(id=id).first()
    if category.is_listed == True:
        category.is_listed = False
        category.save()
    else:
        category.is_listed = True
        category.save()
    return redirect('categorytable')  

def addbrand(request):
    if request.method == 'POST':
        id = request.POST.get('brand_id')
        brand_name = request.POST.get('brand_name')
        brand = Brands(id=id, name=brand_name)
        brand.save()
    
        return redirect('brandtable')
    else:
        return render(request,'adminside/addbrand.html')

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
    
def deletebrand(request,id):
    if request.method == 'POST':
        brand = Brands.objects.filter(id=id)
        brand.delete()
        return redirect('brandtable')
    else:
        return render(request,'adminside/brandtable.html')   

def brand_status(request,id):
    brands = Brands.objects.filter(id=id).first()
    if brands.is_listed == True:
        brands.is_listed = False
        brands.save()
    else:
        brands.is_listed = True
        brands.save()
    return redirect('brandtable')      

        