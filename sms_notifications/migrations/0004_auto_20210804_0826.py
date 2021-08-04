# Generated by Django 3.2.4 on 2021-08-04 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms_notifications', '0003_auto_20210802_0849'),
    ]

    operations = [
        migrations.AddField(
            model_name='smscontacts',
            name='slug',
            field=models.SlugField(default='v7lrac5ubfqgpyxukyc1', verbose_name='Contact Slug'),
        ),
        migrations.AddField(
            model_name='smsgroups',
            name='slug',
            field=models.SlugField(default='2y1opjou8g6uryoe9cqy', verbose_name='Group Slug'),
        ),
        migrations.AddField(
            model_name='smsnotification',
            name='slug',
            field=models.SlugField(default='ihcs5ei0gu7autphfrvi', verbose_name='SMS Slug'),
        ),
    ]
