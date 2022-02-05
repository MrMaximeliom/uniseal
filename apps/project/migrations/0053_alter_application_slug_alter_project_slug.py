# Generated by Django 4.0.1 on 2022-02-01 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0052_alter_application_slug_alter_project_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='slug',
            field=models.SlugField(default='f6df7x', verbose_name='Project Type Slug'),
        ),
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=models.SlugField(default='nnth50', verbose_name='Project Slug'),
        ),
    ]