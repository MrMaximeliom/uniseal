# Generated by Django 4.0.1 on 2022-02-05 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0030_alter_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(default='ile1fesbk2z0rsa5n8og', verbose_name='Product Slug'),
        ),
    ]