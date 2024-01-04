from django.contrib.auth.models import AbstractUser
from django.db import models




class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, null=False)
    date_of_join = models.DateTimeField(auto_now_add=True)
    email_verified = models.BooleanField(default=False)
    email_otp = models.CharField(max_length=6, blank=True, null=True)   
    is_listed = models.BooleanField(default=False)
 
    def __str__(self):
        return self.first_name


