# Generated by Django 4.0.1 on 2022-02-01 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellingPoint', '0028_alter_sellingpoint_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellingpoint',
            name='slug',
            field=models.SlugField(default='pugrzcumoy6nlwn0pshx', verbose_name='Selling Point Slug'),
        ),
    ]