# Generated by Django 3.1.11 on 2021-07-23 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='5nxgp0'),
        ),
    ]
