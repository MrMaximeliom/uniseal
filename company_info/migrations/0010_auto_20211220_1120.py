# Generated by Django 3.1.11 on 2021-12-20 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company_info', '0009_auto_20211220_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyinfo',
            name='slug',
            field=models.SlugField(default='gyzbwfrdowhvvdnjysjg', verbose_name='Company Slug'),
        ),
    ]
