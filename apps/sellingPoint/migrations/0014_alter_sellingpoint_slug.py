# Generated by Django 4.0 on 2022-01-03 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellingPoint', '0013_alter_sellingpoint_id_alter_sellingpoint_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellingpoint',
            name='slug',
            field=models.SlugField(default='865ntyagy5dluuyrr4xz', verbose_name='Selling Point Slug'),
        ),
    ]
