# Generated by Django 4.2.7 on 2024-02-12 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_remove_products_category_offer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='is_listed',
            field=models.BooleanField(default=True),
        ),
    ]