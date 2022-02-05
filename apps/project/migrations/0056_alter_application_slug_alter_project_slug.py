# Generated by Django 4.0.1 on 2022-02-05 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0055_alter_application_slug_alter_project_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='slug',
            field=models.SlugField(default='zizd3j', verbose_name='Project Type Slug'),
        ),
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=models.SlugField(default='ntqelp', verbose_name='Project Slug'),
        ),
    ]