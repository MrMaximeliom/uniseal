# Generated by Django 4.0.5 on 2022-07-18 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0055_alter_user_slug_alter_user_uuid'),
    ]

    operations = [
        # migrations.RemoveField(
        #     model_name='user',
        #     name='working_field',
        # ),
        migrations.AlterField(
            model_name='user',
            name='slug',
            field=models.SlugField(default='awfnclctbbtdfspmji7k', verbose_name='User Slug'),
        ),
    ]
