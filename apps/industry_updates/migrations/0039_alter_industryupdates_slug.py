# Generated by Django 4.0.5 on 2022-07-18 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('industry_updates', '0038_alter_industryupdates_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='industryupdates',
            name='slug',
            field=models.SlugField(default='3e7wnv86fjw210tlfglq', verbose_name='Industry Slug'),
        ),
    ]
