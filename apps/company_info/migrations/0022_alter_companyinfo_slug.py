# Generated by Django 4.0 on 2022-01-10 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company_info', '0021_alter_companyinfo_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyinfo',
            name='slug',
            field=models.SlugField(default='vp0euojlgkhfnc2v6q3o', verbose_name='Company Slug'),
        ),
    ]