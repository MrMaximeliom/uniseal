# Generated by Django 4.0.1 on 2022-02-01 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jop_type', '0002_alter_joptype_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='joptype',
            name='slug',
            field=models.SlugField(default='dghi9ec9nbndtuzptub4', verbose_name='Jop Type Slug'),
        ),
    ]
