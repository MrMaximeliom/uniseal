# Generated by Django 3.2.4 on 2021-08-30 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0023_auto_20210827_1257'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='beneficiary_description',
        ),
        migrations.RemoveField(
            model_name='projectimages',
            name='default_image',
        ),
        migrations.AlterField(
            model_name='application',
            name='slug',
            field=models.SlugField(default='cqu5xm', verbose_name='Project Type Slug'),
        ),
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=models.SlugField(default='shlrfs', verbose_name='Project Slug'),
        ),
    ]
