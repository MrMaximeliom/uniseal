# Generated by Django 4.0 on 2022-01-06 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_alter_cart_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='slug',
            field=models.SlugField(default='order-vmm4zk9p88', verbose_name='Token Slug'),
        ),
    ]