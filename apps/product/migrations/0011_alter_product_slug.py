# Generated by Django 3.2.5 on 2021-07-30 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_alter_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='w1uq2a', verbose_name='Product Slug'),
        ),
    ]
