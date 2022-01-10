# Generated by Django 3.1.11 on 2021-12-20 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0021_auto_20211220_1018'),
    ]

    operations = [
        # migrations.RemoveField(
        #     model_name='city',
        #     name='country',
        # ),
        migrations.AlterField(
            model_name='area',
            name='slug',
            field=models.SlugField(default='t20rzdeg3ofyzdf4o9cz', verbose_name='Area Slug'),
        ),
        migrations.AlterField(
            model_name='city',
            name='slug',
            field=models.SlugField(default='az6jmw019czjzbh9rcvz', verbose_name='City Slug'),
        ),
        migrations.AlterField(
            model_name='country',
            name='slug',
            field=models.SlugField(default='okbj3khgblvczguypixk', verbose_name='Country Slug'),
        ),
        migrations.AlterField(
            model_name='state',
            name='slug',
            field=models.SlugField(default='zp6lxb8yanzzcw7qooju', verbose_name='State Slug'),
        ),
    ]