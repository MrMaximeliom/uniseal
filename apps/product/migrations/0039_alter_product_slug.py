# Generated by Django 4.0 on 2022-01-04 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0038_alter_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='rrnu2luovhvuobzlacuz', verbose_name='Product Slug'),
        ),
    ]