# Generated by Django 4.0 on 2022-01-03 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0034_alter_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='tg4lmueddn38cfifidsh', verbose_name='Product Slug'),
        ),
    ]
