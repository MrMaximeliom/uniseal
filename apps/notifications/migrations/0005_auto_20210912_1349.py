# Generated by Django 3.1.11 on 2021-09-12 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0004_auto_20210910_2023'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notifications',
            old_name='notification_sending_date',
            new_name='notification_date',
        ),
        migrations.AddField(
            model_name='notifications',
            name='notification_time',
            field=models.TimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='notifications',
            name='slug',
            field=models.SlugField(default='f80tcdhz5uvpfz6hoxxs', verbose_name='Notification Slug'),
        ),
        migrations.AlterField(
            model_name='tokenids',
            name='slug',
            field=models.SlugField(default='cmukpk5am35waud3lgou', verbose_name='Token Slug'),
        ),
    ]