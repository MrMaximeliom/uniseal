# Generated by Django 4.0 on 2022-01-07 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0019_alter_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(default='bnvazmoofgypxwubmfj8', verbose_name='Product Slug'),
        ),
    ]
