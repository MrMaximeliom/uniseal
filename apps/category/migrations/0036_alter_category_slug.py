# Generated by Django 4.0.5 on 2022-07-18 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0035_alter_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(default='wdavd4idwvfr1im1ftix', verbose_name='Product Slug'),
        ),
    ]
