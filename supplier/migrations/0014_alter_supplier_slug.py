# Generated by Django 4.0 on 2022-01-03 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0013_alter_supplier_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplier',
            name='slug',
            field=models.SlugField(default='2ch1canuqszfp3trgdsj', verbose_name='Supplier Slug'),
        ),
    ]
