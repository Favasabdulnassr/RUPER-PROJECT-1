from django.contrib import admin
from django.urls import path
from.import views

urlpatterns = [
    path('cart', views.cart, name='cart'),
    path('add_cart',views.add_cart,name='add_cart'),
    path('updateCart',views.update_cart,name='updateCart'),
    path('item_remove',views.remove_item_cart,name='item_remove'),
]

