# Generated by Django 3.1.11 on 2021-09-13 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0026_auto_20210913_1107'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='rank',
            field=models.IntegerField(default=1, verbose_name='Project Order'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='application',
            name='slug',
            field=models.SlugField(default='tw7nwc', verbose_name='Project Type Slug'),
        ),
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=models.SlugField(default='ttofld', verbose_name='Project Slug'),
        ),
    ]
