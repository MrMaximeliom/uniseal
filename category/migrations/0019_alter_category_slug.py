# Generated by Django 4.0 on 2022-01-06 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0018_alter_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(default='v8y4pyyfpriqp6uky57o', verbose_name='Product Slug'),
        ),
    ]
