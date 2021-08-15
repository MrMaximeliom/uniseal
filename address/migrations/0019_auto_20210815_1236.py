# Generated by Django 3.2.4 on 2021-08-15 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0018_auto_20210802_0835'),
    ]

    operations = [
        # migrations.RemoveField(
        #     model_name='city',
        #     name='country',
        # ),
        # migrations.AlterField(
        #     model_name='area',
        #     name='id',
        #     field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        # ),
        migrations.AlterField(
            model_name='area',
            name='slug',
            field=models.SlugField(default='2jimy2jyvpm8arl0cv6f', verbose_name='Area Slug'),
        ),
        # migrations.AlterField(
        #     model_name='city',
        #     name='id',
        #     field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        # ),
        migrations.AlterField(
            model_name='city',
            name='slug',
            field=models.SlugField(default='2xxeunhj2onfb0vzcxri', verbose_name='City Slug'),
        ),
        # migrations.AlterField(
        #     model_name='country',
        #     name='id',
        #     field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        # ),
        migrations.AlterField(
            model_name='country',
            name='slug',
            field=models.SlugField(default='rdupomfjcp0ttvacnfq5', verbose_name='Country Slug'),
        ),
        # migrations.AlterField(
        #     model_name='state',
        #     name='id',
        #     field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        # ),
        migrations.AlterField(
            model_name='state',
            name='slug',
            field=models.SlugField(default='vitthh3gvhqfwxgc22sr', verbose_name='State Slug'),
        ),
    ]
