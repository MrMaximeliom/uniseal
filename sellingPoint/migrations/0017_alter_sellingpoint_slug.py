# Generated by Django 4.0 on 2022-01-04 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellingPoint', '0016_alter_sellingpoint_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellingpoint',
            name='slug',
            field=models.SlugField(default='bgdfjfa0nzi27avzmeio', verbose_name='Selling Point Slug'),
        ),
    ]
