# Generated by Django 4.0.1 on 2022-02-05 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application_videos', '0025_alter_productapplicationvideos_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productapplicationvideos',
            name='slug',
            field=models.SlugField(default='1yfclqnvxfrq7e8galor', verbose_name='Product Video Slug'),
        ),
    ]
