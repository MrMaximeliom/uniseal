# Generated by Django 4.0.1 on 2022-02-06 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application_videos', '0032_alter_productapplicationvideos_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productapplicationvideos',
            name='slug',
            field=models.SlugField(default='pk3f1b9hyofgntbnp3ds', verbose_name='Product Video Slug'),
        ),
    ]