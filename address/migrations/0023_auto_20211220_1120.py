# Generated by Django 3.1.11 on 2021-12-20 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0022_auto_20211220_1026'),
    ]

    operations = [
        # migrations.RemoveField(
        #     model_name='city',
        #     name='country',
        # ),
        migrations.AlterField(
            model_name='area',
            name='slug',
            field=models.SlugField(default='jymsjsdddslftlbleole', verbose_name='Area Slug'),
        ),
        migrations.AlterField(
            model_name='city',
            name='slug',
            field=models.SlugField(default='ewunlgje4tsuhupu11tc', verbose_name='City Slug'),
        ),
        migrations.AlterField(
            model_name='country',
            name='slug',
            field=models.SlugField(default='xmi08jhomftlqo1bgtct', verbose_name='Country Slug'),
        ),
        migrations.AlterField(
            model_name='state',
            name='slug',
            field=models.SlugField(default='1yezx5wuobrrta10bmjc', verbose_name='State Slug'),
        ),
    ]
