# Generated by Django 4.0.1 on 2022-02-05 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0022_alter_order_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='slug',
            field=models.SlugField(default='order-69y74kagq-130329-2022-02-05', verbose_name='Token Slug'),
        ),
    ]
