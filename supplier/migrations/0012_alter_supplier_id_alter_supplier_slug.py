# Generated by Django 4.0 on 2022-01-03 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0011_auto_20211220_1135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplier',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='slug',
            field=models.SlugField(default='vf8iyqhq0eko1n5sfcvw', verbose_name='Supplier Slug'),
        ),
    ]
