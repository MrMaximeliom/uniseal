# Generated by Django 4.0 on 2022-01-10 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brochures', '0022_alter_brochures_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brochures',
            name='slug',
            field=models.SlugField(default='fowdrrecjyvncyhynee2', verbose_name='Brochure Slug'),
        ),
    ]