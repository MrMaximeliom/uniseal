# Generated by Django 4.0.5 on 2022-07-18 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slider', '0035_alter_slider_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slider',
            name='slug',
            field=models.SlugField(default='8utyydcby44uuzyimv4z', verbose_name='Slider Slug'),
        ),
    ]
