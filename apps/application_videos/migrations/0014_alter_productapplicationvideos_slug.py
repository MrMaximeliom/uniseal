# Generated by Django 4.0 on 2022-01-04 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application_videos', '0013_alter_productapplicationvideos_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productapplicationvideos',
            name='slug',
            field=models.SlugField(default='68b9l2avzj0fds1cfcho', verbose_name='Product Video Slug'),
        ),
    ]
