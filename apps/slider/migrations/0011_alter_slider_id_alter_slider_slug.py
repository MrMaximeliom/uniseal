# Generated by Django 4.0 on 2022-01-03 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slider', '0010_auto_20211220_1135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slider',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='slider',
            name='slug',
            field=models.SlugField(default='vcfkp6usnfdxtrfelasn', verbose_name='Slider Slug'),
        ),
    ]