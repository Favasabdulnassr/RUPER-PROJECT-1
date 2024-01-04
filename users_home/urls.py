from django.contrib import admin
from django.urls import path
from.import views

urlpatterns = [
path('',views.Home,name='home'),  
path('shop/',views.shop, name='shop'),
path('contact/', views.contact, name='contact'),
path('aboutus/',views.aboutus, name='aboutus'),
path('wishlist/',views.wishlist,name='wishlist'),
path('shopdetails/<str:id>',views.shopdetails, name='shopdetails')
]

