from django.contrib import admin
from django.urls import path
from.import views

urlpatterns = [
path('', views.Home, name = 'home'),
path('signup/',views.signup, name = 'signup'),
path('otp_verification/<str:username>/', views.otp_verification, name='otp_verification'),
path('login/',views.login, name ='login'),
path('home1/',views.Home1, name='home1'),
path('logout/', views.logout, name='logout'),
path('shop/',views.shop, name='shop'),
path('contact/', views.contact, name='contact'),
path('myaccount/', views.myaccount, name='myaccount'),
path('aboutus/',views.aboutus, name='aboutus'),
path('wishlist/',views.wishlist,name='wishlist'),
path('cart/',views.cart, name='cart'),
path('checkout/', views.checkout, name='checkout'),
path('shopdetails/',views.shopdetails, name='shopdetails')
]

