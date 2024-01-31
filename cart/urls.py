from django.contrib import admin
from django.urls import path
from.import views

urlpatterns = [
    path('cart', views.cart, name='cart'),
    path('add_cart',views.add_cart,name='add_cart'),
    path('updateCart',views.update_cart,name='updateCart'),
    path('item_remove',views.remove_item_cart,name='item_remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('editAddress/<str:id>',views.edit_address,name='editAddress'),
    path('addAddress/',views.add_address,name='addAddress'),
    path('apply_coupon',views.apply_coupon,name='apply_coupon'),
    path('remove_coupon',views.remove_coupon,name='remove_coupon'),
   

]

