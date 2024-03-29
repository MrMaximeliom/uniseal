# Generated by Django 3.2.4 on 2021-09-05 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company_info', '0005_auto_20210815_1254'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyinfo',
            name='about',
            field=models.TextField(blank=True, null=True, verbose_name='About Company'),
        ),
        migrations.AlterField(
            model_name='companyinfo',
            name='slug',
            field=models.SlugField(default='aeyqpd5k9qak3l5vxxmr', verbose_name='Company Slug'),
        ),
    ]
