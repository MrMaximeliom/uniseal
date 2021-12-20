# Generated by Django 3.1.11 on 2021-12-20 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellingPoint', '0011_auto_20211220_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellingpoint',
            name='arabic_name',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Sale Point Name(Arabic)'),
        ),
        migrations.AlterField(
            model_name='sellingpoint',
            name='slug',
            field=models.SlugField(default='dhhewlnhegb7hzvsnynr', verbose_name='Selling Point Slug'),
        ),
    ]
