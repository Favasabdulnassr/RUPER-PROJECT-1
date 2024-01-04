from django.contrib import admin
from django.urls import path
from.import views

urlpatterns = [
    path('order_success/',views.order_successfull,name='order_success'),
    path('place_order/',views.placer_order,name='place_order'),
    path('cancel_order/<int:id>/',views.cancel_order,name='cancel_order'),
    
]

