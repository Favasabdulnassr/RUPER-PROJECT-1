# Generated by Django 4.2.7 on 2024-01-01 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userAuthentication', '0006_customuser_is_listed'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='email_otp_timestamp',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
