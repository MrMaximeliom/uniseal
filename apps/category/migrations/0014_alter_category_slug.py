# Generated by Django 4.0 on 2022-01-03 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0013_alter_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(default='ezahlgbanwh5v75wde0i', verbose_name='Product Slug'),
        ),
    ]
