# Generated by Django 4.0.1 on 2022-02-01 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_order_total_alter_order_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='slug',
            field=models.SlugField(default='order-2hk8and95-094312-2022-02-01', verbose_name='Token Slug'),
        ),
    ]