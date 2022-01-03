# Generated by Django 4.0 on 2022-01-03 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0040_alter_application_slug_alter_project_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='slug',
            field=models.SlugField(default='igfv7r', verbose_name='Project Type Slug'),
        ),
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=models.SlugField(default='gpdv0i', verbose_name='Project Slug'),
        ),
    ]
