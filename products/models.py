from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    is_listed = models.BooleanField

    def __str__(self):
        return self.name

class Brands(models.Model):
    name = models.CharField(max_length=50)
    is_listed = models.BooleanField
    
    def __str__(self):
        return self.name


class Products(models.Model):
    products_name = models.CharField(max_length=50)
    category_id = models.ForeignKey(Category,on_delete=models.CASCADE,)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    brand_id = models.ForeignKey(Brands,on_delete=models.CASCADE)
    is_listed = models.BooleanField(default=True)
    colour = models.CharField(max_length=50)

    def __str__(self):
        return self.products_name
    
class Image(models.Model):
    image = models.ImageField(upload_to="product_images")
    product_id = models.ForeignKey(Products,on_delete=models.CASCADE)




