# Generated by Django 4.0.1 on 2022-02-05 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0032_alter_supplier_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplier',
            name='slug',
            field=models.SlugField(default='7y7v5axuro5nzzomtdna', verbose_name='Supplier Slug'),
        ),
    ]