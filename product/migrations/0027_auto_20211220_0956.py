# Generated by Django 3.1.11 on 2021-12-20 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0026_auto_20210919_0831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='h9k8oio7qykubpw0a6wf', verbose_name='Product Slug'),
        ),
    ]
