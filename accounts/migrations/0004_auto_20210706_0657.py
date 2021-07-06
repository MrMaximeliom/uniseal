# Generated by Django 3.2.4 on 2021-07-06 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20210704_0717'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='area',
        ),
        migrations.AddField(
            model_name='user',
            name='working_field',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Working Field'),
        ),
    ]
