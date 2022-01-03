# Generated by Django 4.0 on 2022-01-03 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0037_auto_20211220_1135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='application',
            name='slug',
            field=models.SlugField(default='sxs4tv', verbose_name='Project Type Slug'),
        ),
        migrations.AlterField(
            model_name='project',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=models.SlugField(default='e9lovi', verbose_name='Project Slug'),
        ),
        migrations.AlterField(
            model_name='projectimages',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='projectsolutions',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='projectvideos',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
