# Generated by Django 4.0.1 on 2022-02-01 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0028_alter_notifications_slug_alter_tokenids_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notifications',
            name='slug',
            field=models.SlugField(default='v6qhlsggoul5viakh8zf', verbose_name='Notification Slug'),
        ),
        migrations.AlterField(
            model_name='tokenids',
            name='slug',
            field=models.SlugField(default='kfojzf8oghcn6xln3wdu', verbose_name='Token Slug'),
        ),
    ]