# Generated by Django 4.0 on 2022-01-06 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company_info', '0018_alter_companyinfo_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyinfo',
            name='slug',
            field=models.SlugField(default='2av6bbnjxi6jm9hh4ej3', verbose_name='Company Slug'),
        ),
    ]