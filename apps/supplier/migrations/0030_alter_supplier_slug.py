# Generated by Django 4.0.1 on 2022-02-05 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0029_alter_supplier_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplier',
            name='slug',
            field=models.SlugField(default='ium4uur5wsjrgtfvkv2p', verbose_name='Supplier Slug'),
        ),
    ]