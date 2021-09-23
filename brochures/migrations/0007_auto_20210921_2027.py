# Generated by Django 3.1.11 on 2021-09-21 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brochures', '0006_auto_20210817_2054'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brochures',
            name='image',
        ),
        migrations.AlterField(
            model_name='brochures',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='brochures',
            name='slug',
            field=models.SlugField(default='awr1aq0pgcnepwxxo0mz', verbose_name='Brochure Slug'),
        ),
    ]