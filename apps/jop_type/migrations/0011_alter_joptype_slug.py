# Generated by Django 4.0.1 on 2022-02-05 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jop_type', '0010_alter_joptype_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joptype',
            name='slug',
            field=models.SlugField(default='oqdcpdlhd3qwrwzvlmd3', verbose_name='Job Type Slug'),
        ),
    ]
