# Generated by Django 4.0.1 on 2022-02-05 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0020_alter_order_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='slug',
            field=models.SlugField(default='order-9ov37d7hk-112504-2022-02-05', verbose_name='Token Slug'),
        ),
    ]
