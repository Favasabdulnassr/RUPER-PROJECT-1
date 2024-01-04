from django.db import models
from userAuthentication.models import*
from products.models import *
# 

class Cart(models.Model):
    customuser = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(null=False,blank=False,default=1)
    cart_price = models.PositiveBigIntegerField(default=1)

   
    