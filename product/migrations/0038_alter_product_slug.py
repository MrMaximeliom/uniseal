# Generated by Django 4.0 on 2022-01-04 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0037_alter_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='5bhhbndagmobring5xgr', verbose_name='Product Slug'),
        ),
    ]
