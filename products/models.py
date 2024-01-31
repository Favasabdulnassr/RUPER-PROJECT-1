from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    is_listed = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Brands(models.Model):
    name = models.CharField(max_length=50)
    is_listed = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name


class Products(models.Model):
    products_name = models.CharField(max_length=50)
    category_id = models.ForeignKey(Category,on_delete=models.CASCADE,)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    brand_id = models.ForeignKey(Brands,on_delete=models.CASCADE)
    is_listed = models.BooleanField(default=False)
    product_offer = models.PositiveIntegerField(default = 0)


    def discounted_price(self):
        discount_percentage = self.product_offer
        if discount_percentage > 0:
            return self.price - ((self.price * discount_percentage) / 100)
        else:
            return self.price
        

    def __str__(self):
        return self.products_name
    
class Image(models.Model):
    image = models.ImageField(upload_to="product_images")
    product_id = models.ForeignKey(Products,on_delete=models.CASCADE)
    




