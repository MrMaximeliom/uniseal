# Generated by Django 3.1.11 on 2021-12-20 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application_videos', '0007_auto_20211220_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productapplicationvideos',
            name='slug',
            field=models.SlugField(default='vqkpo3bvxczf01zzebzk', verbose_name='Product Video Slug'),
        ),
    ]
