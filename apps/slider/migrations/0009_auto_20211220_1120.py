# Generated by Django 3.1.11 on 2021-12-20 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slider', '0008_auto_20211220_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slider',
            name='slug',
            field=models.SlugField(default='czm0irwe7r1mnt8uh1mj', verbose_name='Slider Slug'),
        ),
    ]
