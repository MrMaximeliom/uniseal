# Generated by Django 4.0.1 on 2022-02-01 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('industry_updates', '0026_alter_industryupdates_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='industryupdates',
            name='slug',
            field=models.SlugField(default='nwiltdeumoztb9pble9n', verbose_name='Industry Slug'),
        ),
    ]