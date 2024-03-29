# Generated by Django 3.1.11 on 2021-12-20 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0005_alter_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(default='4v3g1kekisqwsnagsu4t', verbose_name='Product Slug'),
        ),
    ]
