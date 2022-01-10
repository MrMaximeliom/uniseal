# Generated by Django 3.1.11 on 2021-12-20 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0010_auto_20211220_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplier',
            name='arabic_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Supplier Name(Arabic)'),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='slug',
            field=models.SlugField(default='dqt7dcmy6pd1302akzd2', verbose_name='Supplier Slug'),
        ),
    ]