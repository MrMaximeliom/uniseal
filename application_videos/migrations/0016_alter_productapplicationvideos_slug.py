# Generated by Django 4.0 on 2022-01-06 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application_videos', '0015_alter_productapplicationvideos_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productapplicationvideos',
            name='slug',
            field=models.SlugField(default='jqyfci0leldr17kzmcdm', verbose_name='Product Video Slug'),
        ),
    ]
