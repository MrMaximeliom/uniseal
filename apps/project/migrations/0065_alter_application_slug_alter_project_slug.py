# Generated by Django 4.0.5 on 2022-07-18 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0064_alter_application_slug_alter_project_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='slug',
            field=models.SlugField(default='d4qzdf', verbose_name='Project Type Slug'),
        ),
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=models.SlugField(default='kxzjmj', verbose_name='Project Slug'),
        ),
    ]
