# Generated by Django 4.0 on 2022-01-04 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application_videos', '0014_alter_productapplicationvideos_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productapplicationvideos',
            name='slug',
            field=models.SlugField(default='6uggodpdxsiffpoxvbyb', verbose_name='Product Video Slug'),
        ),
    ]
