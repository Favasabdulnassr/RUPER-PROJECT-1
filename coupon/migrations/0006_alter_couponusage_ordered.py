# Generated by Django 4.2.7 on 2024-01-24 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0005_couponusage_ordered'),
    ]

    operations = [
        migrations.AlterField(
            model_name='couponusage',
            name='ordered',
            field=models.PositiveIntegerField(default=0),
        ),
    ]