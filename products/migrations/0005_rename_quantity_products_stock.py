# Generated by Django 4.2.7 on 2023-12-14 11:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_brands_is_listed_category_is_listed'),
    ]

    operations = [
        migrations.RenameField(
            model_name='products',
            old_name='quantity',
            new_name='stock',
        ),
    ]
