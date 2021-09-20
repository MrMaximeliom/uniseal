# Generated by Django 3.1.11 on 2021-09-20 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0027_auto_20210913_1324'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='image',
        ),
        migrations.AlterField(
            model_name='application',
            name='slug',
            field=models.SlugField(default='da7ofe', verbose_name='Project Type Slug'),
        ),
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=models.SlugField(default='a6d8ea', verbose_name='Project Slug'),
        ),
    ]
