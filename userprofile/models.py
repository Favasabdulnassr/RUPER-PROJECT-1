from django.db import models
from userAuthentication.models import CustomUser

# Create your models here.

class Address(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    street_address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pin_code = models.IntegerField()

    def __self__(self):
        return f"Address for {self.user.email}"
