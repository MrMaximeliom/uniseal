# Generated by Django 4.0.1 on 2022-02-01 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slider', '0023_alter_slider_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slider',
            name='slug',
            field=models.SlugField(default='vvhwdiifnrwdxtbvqejp', verbose_name='Slider Slug'),
        ),
    ]