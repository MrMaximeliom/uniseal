# Generated by Django 3.2.4 on 2021-08-16 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms_notifications', '0009_auto_20210816_0726'),
    ]

    operations = [
        migrations.AddField(
            model_name='smsgroupmessages',
            name='status',
            field=models.CharField(blank=True, max_length=11, null=True, verbose_name='SMS Status'),
        ),
        # migrations.AddField(
        #     model_name='smsnotification',
        #     name='status',
        #     field=models.CharField(blank=True, max_length=11, null=True, verbose_name='SMS Status'),
        # ),
        migrations.AlterField(
            model_name='smscontacts',
            name='slug',
            field=models.SlugField(default='ei6q47l9gb3c8wxlsd33', verbose_name='Contact Slug'),
        ),
        migrations.AlterField(
            model_name='smsgroupmessages',
            name='slug',
            field=models.SlugField(default='tebhbjkqrao411yodnho', verbose_name='SMS Group Message Slug'),
        ),
        migrations.AlterField(
            model_name='smsgroups',
            name='slug',
            field=models.SlugField(default='j0k96w2qltvmf7vyi07g', verbose_name='Group Slug'),
        ),
        migrations.AlterField(
            model_name='smsnotification',
            name='slug',
            field=models.SlugField(default='gw9lmn1xahphlnj6b4gm', verbose_name='SMS Slug'),
        ),
    ]
