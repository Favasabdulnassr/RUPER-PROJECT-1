# Generated by Django 4.2.7 on 2023-12-04 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userAuthentication', '0005_customuser_email_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_listed',
            field=models.BooleanField(default=False),
        ),
    ]