from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid




class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, null=False)
    date_of_join = models.DateTimeField(auto_now_add=True)
    email_verified = models.BooleanField(default=False)
    email_otp = models.CharField(max_length=6, blank=True, null=True)   
    is_listed = models.BooleanField(default=False)
    referal_id = models.CharField(max_length=7, unique=True, editable=False,null=True,blank=True)
    reffered = models.PositiveIntegerField(default=0)
    reffered_id = models.CharField(max_length=7,blank=True, null=True)

    def save(self,*args,**kwargs):
        if not self.referal_id:
            self.referal_id = self.generate_referal_id()
        super().save(*args,**kwargs)


    def generate_referal_id(self):
        return str(uuid.uuid4().hex)[:6]
 
    def __str__(self):
        return self.first_name


