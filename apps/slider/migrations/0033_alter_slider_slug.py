# Generated by Django 4.0.1 on 2022-02-05 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slider', '0032_alter_slider_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slider',
            name='slug',
            field=models.SlugField(default='pdvkmbyk0g9sv4697zsb', verbose_name='Slider Slug'),
        ),
    ]
