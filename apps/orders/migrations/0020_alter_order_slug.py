# Generated by Django 4.0.1 on 2022-02-05 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0019_alter_order_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='slug',
            field=models.SlugField(default='order-ah0bi59v2-112147-2022-02-05', verbose_name='Token Slug'),
        ),
    ]