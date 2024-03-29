# Generated by Django 4.0 on 2022-02-10 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0064_product_price_alter_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(default='0.0', null=True, verbose_name='Price'),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='rwcturzkzdyqankykxlj', verbose_name='Product Slug'),
        ),
    ]
