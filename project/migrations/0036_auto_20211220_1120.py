# Generated by Django 3.1.11 on 2021-12-20 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0035_auto_20211220_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='slug',
            field=models.SlugField(default='fvxipj', verbose_name='Project Type Slug'),
        ),
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=models.SlugField(default='crxe3r', verbose_name='Project Slug'),
        ),
    ]