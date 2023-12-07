from django.contrib import admin
from django.urls import path
from.import views

urlpatterns = [
    path('', views.adminlogin, name= 'adminlogin'),
    path('usertable/', views.usertable, name='usertable'),
    path('productable/',views.productable, name='productable'),
    path('logoutadmin/',views.logoutadmin, name='logoutadmin'),
    path('categorytable/',views.categorytable, name='categorytable'),
    path('brandtable/',views.brandtable, name='brandtable'),
]
