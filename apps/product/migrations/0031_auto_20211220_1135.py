# Generated by Django 3.1.11 on 2021-12-20 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0030_auto_20211220_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='arabic_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Product Name(Arabic)'),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='vfrk7bbxinynpdqxoudi', verbose_name='Product Slug'),
        ),
    ]
