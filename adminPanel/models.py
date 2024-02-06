from django.db import models

class Banner(models.Model):
    banner_image = models.ImageField(upload_to='banner')

    

    

# Create your models here.
