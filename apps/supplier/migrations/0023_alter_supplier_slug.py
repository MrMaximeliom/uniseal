# Generated by Django 4.0.1 on 2022-02-01 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0022_alter_supplier_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplier',
            name='slug',
            field=models.SlugField(default='l423ijr9y7njgoyfc2sd', verbose_name='Supplier Slug'),
        ),
    ]
