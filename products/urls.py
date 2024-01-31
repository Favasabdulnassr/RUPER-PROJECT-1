from django.urls import path, include
from django.conf import settings
from .import views

urlpatterns = [
    path('product_offers/',views.product_offers,name='product_offers'),
    path('add_product_offers/',views.add_product_offers,name='add_product_offers'),
    path('edit_product_offers/<str:id>',views.edit_product_offer,name='edit_product_offers'),
    path('cancel_product_offers/<str:id>',views.cancel_product_offer,name='cancel_product_offer'),

]
