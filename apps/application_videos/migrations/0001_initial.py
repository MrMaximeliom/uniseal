# Generated by Django 3.2.4 on 2021-08-24 07:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0020_alter_product_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductApplicationVideos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('application_video', models.URLField(verbose_name='Product Video Url')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product', verbose_name='Product')),
            ],
        ),
    ]
