# Generated by Django 4.0.1 on 2022-02-05 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellingPoint', '0034_alter_sellingpoint_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellingpoint',
            name='slug',
            field=models.SlugField(default='ku805vjgkxubonruirfy', verbose_name='Selling Point Slug'),
        ),
    ]
