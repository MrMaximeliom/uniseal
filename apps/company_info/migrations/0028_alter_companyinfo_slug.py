# Generated by Django 4.0.1 on 2022-02-01 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company_info', '0027_alter_companyinfo_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyinfo',
            name='slug',
            field=models.SlugField(default='umhhyursv1vchr2j1jra', verbose_name='Company Slug'),
        ),
    ]
