# Generated by Django 4.0 on 2022-01-03 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0012_alter_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(default='rvdjklj8fddlzooz9lgs', verbose_name='Product Slug'),
        ),
    ]