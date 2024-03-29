# Generated by Django 3.1.11 on 2021-12-20 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0009_auto_20211220_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='arabic_name',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='Category Name (Arabic)'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(default='pr8peb5y56xh2yeeyfde', verbose_name='Product Slug'),
        ),
    ]
