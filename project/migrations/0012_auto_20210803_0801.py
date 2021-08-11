# Generated by Django 3.2.4 on 2021-08-03 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0011_auto_20210803_0629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='execution_date',
            field=models.CharField(max_length=200, verbose_name='Execution Year'),
        ),
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=models.SlugField(default='f4nnr0', verbose_name='Project Slug'),
        ),
    ]