# Generated by Django 4.0.5 on 2022-07-18 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jop_type', '0014_alter_joptype_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joptype',
            name='slug',
            field=models.SlugField(default='g2ks0c2v7esabtmu5jbp', verbose_name='Job Type Slug'),
        ),
    ]
