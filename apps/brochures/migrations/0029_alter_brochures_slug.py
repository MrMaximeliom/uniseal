# Generated by Django 4.0.1 on 2022-02-01 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brochures', '0028_alter_brochures_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brochures',
            name='slug',
            field=models.SlugField(default='2oggw3rejylzo0h5cqlu', verbose_name='Brochure Slug'),
        ),
    ]
