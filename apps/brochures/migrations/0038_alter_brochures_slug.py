# Generated by Django 4.0 on 2022-02-10 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brochures', '0037_alter_brochures_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brochures',
            name='slug',
            field=models.SlugField(default='jzxletibmpsgvymrtfga', verbose_name='Brochure Slug'),
        ),
    ]