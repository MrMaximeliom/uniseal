# Generated by Django 4.0.1 on 2022-02-05 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jop_type', '0007_alter_joptype_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joptype',
            name='slug',
            field=models.SlugField(default='zwvfbcg9yyhb0pihw3nz', verbose_name='Job Type Slug'),
        ),
    ]
