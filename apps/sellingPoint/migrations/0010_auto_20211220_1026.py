# Generated by Django 3.1.11 on 2021-12-20 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellingPoint', '0009_auto_20211220_1018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellingpoint',
            name='slug',
            field=models.SlugField(default='wlovfolaz0x3efnpj42q', verbose_name='Selling Point Slug'),
        ),
    ]