# Generated by Django 4.0.1 on 2022-02-01 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slider', '0025_alter_slider_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slider',
            name='slug',
            field=models.SlugField(default='masvqt4lwq125htynkkp', verbose_name='Slider Slug'),
        ),
    ]
