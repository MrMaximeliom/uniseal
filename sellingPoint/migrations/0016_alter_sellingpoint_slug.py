# Generated by Django 4.0 on 2022-01-03 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellingPoint', '0015_alter_sellingpoint_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellingpoint',
            name='slug',
            field=models.SlugField(default='szar6sar1ctzyy0golxm', verbose_name='Selling Point Slug'),
        ),
    ]
