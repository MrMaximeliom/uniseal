# Generated by Django 4.0.1 on 2022-02-06 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0034_alter_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(default='kxad7yc0r2akgosmdm2v', verbose_name='Product Slug'),
        ),
    ]
