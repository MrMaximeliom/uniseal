# Generated by Django 4.0.1 on 2022-02-01 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0046_alter_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='h7tcvfbldsjx7eavuv1d', verbose_name='Product Slug'),
        ),
    ]