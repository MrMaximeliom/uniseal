# Generated by Django 4.0.5 on 2022-07-18 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0027_alter_order_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='slug',
            field=models.SlugField(default='order-n4w16r5xa-120511-2022-07-18', verbose_name='Token Slug'),
        ),
    ]
