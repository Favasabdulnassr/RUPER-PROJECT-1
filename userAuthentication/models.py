from django.contrib.auth.models import AbstractUser
from django.db import models
import random
from django.core.mail import send_mail
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.loader import render_to_string




class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, null=False)
    date_of_join = models.DateTimeField(auto_now_add=True)
    email_verified = models.BooleanField(default=False)
    email_otp = models.CharField(max_length=6, blank=True, null=True)   
    is_listed = models.BooleanField(default=False)
 
    def __str__(self):
        return self.username

# Create a signal handler to send OTP via email

    
@receiver(post_save, sender=CustomUser)
def send_otp(instance, created, **kwargs):
    if created:
        # Generate OTP
        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        instance.email_otp = otp
        instance.save()
        html_message = render_to_string('userside/email_otp.html', {'otp':otp})  # Render the HTML template


        # Send OTP via Email
        send_mail(
            'Email Verification OTP',
            '',
            settings.EMAIL_HOST_USER,  # Sender's email
            [instance.email],  # Receiver's email
            fail_silently=False,
            html_message=html_message
        )

# Signal receiver to trigger send_otp function
models.signals.post_save.connect(send_otp, sender=CustomUser)
