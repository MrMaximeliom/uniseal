# Generated by Django 4.0.1 on 2022-02-01 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0026_alter_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(default='n4npmuk7abzqbfcfsnew', verbose_name='Product Slug'),
        ),
    ]