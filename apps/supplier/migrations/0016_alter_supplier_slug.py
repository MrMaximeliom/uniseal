# Generated by Django 4.0 on 2022-01-04 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0015_alter_supplier_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplier',
            name='slug',
            field=models.SlugField(default='rshcif4dfq2oac2txjyl', verbose_name='Supplier Slug'),
        ),
    ]
