# Generated by Django 4.0.1 on 2022-02-05 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brochures', '0030_alter_brochures_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brochures',
            name='slug',
            field=models.SlugField(default='1evxhwbvhcbkxp6sbssp', verbose_name='Brochure Slug'),
        ),
    ]
