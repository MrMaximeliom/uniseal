# Generated by Django 4.0.1 on 2022-02-09 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request_permissions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestaccess',
            name='status',
            field=models.BooleanField(blank=True, default=False, verbose_name='Access Status'),
        ),
    ]