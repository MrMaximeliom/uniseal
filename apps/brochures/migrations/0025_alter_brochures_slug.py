# Generated by Django 4.0.1 on 2022-02-01 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brochures', '0024_alter_brochures_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brochures',
            name='slug',
            field=models.SlugField(default='fxobaz3vbdxzmx8wyj1g', verbose_name='Brochure Slug'),
        ),
    ]