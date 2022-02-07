# Generated by Django 4.0.1 on 2022-02-06 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0036_alter_notifications_slug_alter_tokenids_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notifications',
            name='slug',
            field=models.SlugField(default='tfh0vevktxox2hympyw8', verbose_name='Notification Slug'),
        ),
        migrations.AlterField(
            model_name='tokenids',
            name='slug',
            field=models.SlugField(default='szh5sbbqtdpvaa9hn4o6', verbose_name='Token Slug'),
        ),
    ]