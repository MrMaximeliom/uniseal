# Generated by Django 3.2.4 on 2021-08-15 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms_notifications', '0005_auto_20210805_1535'),
    ]

    operations = [
        migrations.AddField(
            model_name='smsnotification',
            name='status',
            field=models.CharField(blank=True, max_length=11, null=True, verbose_name='SMS Status'),
        ),
        migrations.AlterField(
            model_name='smscontacts',
            name='slug',
            field=models.SlugField(default='3z4ahyrv3qa9m26rpcwf', verbose_name='Contact Slug'),
        ),
        migrations.AlterField(
            model_name='smsgroups',
            name='slug',
            field=models.SlugField(default='fkxkaj0xoajyh89ttzgv', verbose_name='Group Slug'),
        ),
        migrations.AlterField(
            model_name='smsnotification',
            name='slug',
            field=models.SlugField(default='14pmbuffueaozz7cxvvi', verbose_name='SMS Slug'),
        ),
    ]
