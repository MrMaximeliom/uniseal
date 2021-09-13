# Generated by Django 3.1.11 on 2021-09-13 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0025_auto_20210830_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectimages',
            name='is_default',
            field=models.BooleanField(default=False, verbose_name='Default Image?'),
        ),
        migrations.AlterField(
            model_name='application',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='application',
            name='slug',
            field=models.SlugField(default='mlpoan', verbose_name='Project Type Slug'),
        ),
        migrations.AlterField(
            model_name='project',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=models.SlugField(default='e1sbnn', verbose_name='Project Slug'),
        ),
        migrations.AlterField(
            model_name='projectimages',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='projectsolutions',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='projectvideos',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
