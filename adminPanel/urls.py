from django.contrib import admin
from django.urls import path
from.import views

urlpatterns = [
    path('adminlogin/', views.adminlogin, name= 'adminlogin'),
    path('usertable/', views.usertable, name='usertable'),
    path('producttable/',views.producttable, name='producttable'),
    path('logoutadmin/',views.logoutadmin, name='logoutadmin'),
    path('categorytable/',views.categorytable, name='categorytable'),
    path('brandtable/',views.brandtable, name='brandtable'),
    path('addproduct/',views.addproduct, name= 'addproduct'),
    path('editproduct/<str:id>',views.editproduct,name='editproduct'),
    path('deleteproduct/<str:id>',views.deleteproduct,name='deleteproduct'),
    path('product_status/<str:id>',views.product_status,name='product_status'),
    path('user_status/<str:id>',views.user_status,name='user_status'),
    path('addcategory/',views.addcategory,name='addcategory'),
    path('editcategory/<str:id>',views.editcategory,name='editcategory'),
    path('deletecategory/<str:id>',views.deletecategory,name='deletecategory'),
    path('category_status/<str:id>',views.category_status,name="category_status"),
    path('addbrand/',views.addbrand,name='addbrand'),
    path('editbrand/<str:id>',views.editbrand,name='editbrand'),
    path('deletebrand/<str:id>',views.deletebrand,name='deletebrand'),
    path('brand_status/<str:id>',views.brand_status,name='brand_status'),
    path('orders',views.orders,name='orders'),
    path('order_details/<str:id>/',views.order_details,name='order_details')
]
