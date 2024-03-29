# Generated by Django 4.0 on 2022-02-10 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0061_alter_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=7, null=True, verbose_name='Price'),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='pp9wb0q7pb8qcqk0twg7', verbose_name='Product Slug'),
        ),
    ]
