# Generated by Django 3.1.11 on 2021-12-20 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0008_auto_20211220_0956'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='arabic_title',
            field=models.CharField(max_length=250, null=True, verbose_name='Notification Title(Arabic)'),
        ),
        migrations.AlterField(
            model_name='notifications',
            name='slug',
            field=models.SlugField(default='u1jlnug9wyif0o8biu3r', verbose_name='Notification Slug'),
        ),
        migrations.AlterField(
            model_name='tokenids',
            name='slug',
            field=models.SlugField(default='55ugvphjg0lc6bkmr1zo', verbose_name='Token Slug'),
        ),
    ]
