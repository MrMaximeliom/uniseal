# Generated by Django 3.1.11 on 2021-12-20 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellingPoint', '0008_auto_20211220_0956'),
    ]

    operations = [
        migrations.AddField(
            model_name='sellingpoint',
            name='arabic_name',
            field=models.CharField(max_length=150, null=True, verbose_name='Sale Point Name(Arabic)'),
        ),
        migrations.AlterField(
            model_name='sellingpoint',
            name='slug',
            field=models.SlugField(default='kblen0mlap99ybrri47g', verbose_name='Selling Point Slug'),
        ),
    ]
