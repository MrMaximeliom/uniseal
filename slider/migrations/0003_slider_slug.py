# Generated by Django 3.2.5 on 2021-07-30 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slider', '0002_alter_slider_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='slider',
            name='slug',
            field=models.SlugField(default='u4q1jf', verbose_name='Slider Slug'),
        ),
    ]