# Generated by Django 3.1.11 on 2021-12-20 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms_notifications', '0014_auto_20211220_1120'),
    ]

    operations = [
        # migrations.AddField(
        #     model_name='smsnotification',
        #     name='status',
        #     field=models.CharField(blank=True, max_length=11, null=True, verbose_name='SMS Status'),
        # ),
        migrations.AlterField(
            model_name='smscontacts',
            name='slug',
            field=models.SlugField(default='taexl1lj5c6etsg29eqi', verbose_name='Contact Slug'),
        ),
        migrations.AlterField(
            model_name='smsgroupmessages',
            name='slug',
            field=models.SlugField(default='rcv33mdp3tt2tpgvfvts', verbose_name='SMS Group Message Slug'),
        ),
        migrations.AlterField(
            model_name='smsgroups',
            name='arabic_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Group Name(Arabic)'),
        ),
        migrations.AlterField(
            model_name='smsgroups',
            name='slug',
            field=models.SlugField(default='ypnef2r0afhnnhwvcsmv', verbose_name='Group Slug'),
        ),
        migrations.AlterField(
            model_name='smsnotification',
            name='slug',
            field=models.SlugField(default='5vaqrntbzbvdkoea2vze', verbose_name='SMS Slug'),
        ),
    ]
