# Generated by Django 4.0.1 on 2022-02-01 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application_videos', '0022_alter_productapplicationvideos_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productapplicationvideos',
            name='slug',
            field=models.SlugField(default='tlre06mz3gmy1ecc1cyx', verbose_name='Product Video Slug'),
        ),
    ]
