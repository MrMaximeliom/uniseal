# Generated by Django 3.2.4 on 2021-08-17 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0020_auto_20210815_1236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='name',
            field=models.CharField(max_length=300, verbose_name='Project Type'),
        ),
        migrations.AlterField(
            model_name='application',
            name='slug',
            field=models.SlugField(default='3ppjco', verbose_name='Project Type Slug'),
        ),
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=models.SlugField(default='febjta', verbose_name='Project Slug'),
        ),
    ]
