# Generated by Django 4.0.1 on 2022-02-05 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0027_alter_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(default='8rujdtizqnketkcktu0z', verbose_name='Product Slug'),
        ),
    ]