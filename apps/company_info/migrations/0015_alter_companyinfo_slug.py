# Generated by Django 4.0 on 2022-01-03 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company_info', '0014_alter_companyinfo_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyinfo',
            name='slug',
            field=models.SlugField(default='vz6cdgvzbfxv9zf0pbun', verbose_name='Company Slug'),
        ),
    ]
