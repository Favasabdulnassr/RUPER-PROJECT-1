from django.db import models
from userAuthentication.models import CustomUser
from userprofile.models import Address
import uuid
from products.models import Products

# Create your models here.

class Orders(models.Model):
    order_id = models.CharField(max_length=8,primary_key=True,unique=True,editable=False)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    address = models.ForeignKey(Address,on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=200)
    order_date = models.DateTimeField(auto_now_add=True)
    expected_delivery_date = models.DateField(null=True,blank=True)
    delivered_date = models.DateTimeField(null=True,blank=True)
    quantity = models.PositiveIntegerField()
    total_purchase_amount = models.PositiveIntegerField(default=1)

    def save(self,*args,**kwargs):
        if not self.order_id:
            self.order_id = self.generate_order_id()
        super().save(*args,**kwargs)

    def generate_order_id(self):     
        return str(uuid.uuid4().hex)[:8]
    
    
    def __str__(self) -> str:
        return f"{self.user}'s order details"
    


class OrdersItem(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    payment_status =models.CharField(max_length=255, default='pending')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    updated_time = models.DateTimeField(auto_now=True)
    quantity = models.PositiveBigIntegerField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    total_item_amount = models.PositiveBigIntegerField(default=1)   
    status = models.CharField(default='Order confirmed',max_length=200)
    def total_price(self):
        return self.quantity * self.price

    def __str__(self) -> str:
        return f"{self.order.user}'s {self.product}"    
    






    
    
    
    
  