# Generated by Django 4.0.1 on 2022-02-05 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0028_alter_supplier_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplier',
            name='slug',
            field=models.SlugField(default='3vy6okjjstgoizblckje', verbose_name='Supplier Slug'),
        ),
    ]
