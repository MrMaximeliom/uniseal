# Generated by Django 4.0.1 on 2022-02-05 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('industry_updates', '0035_alter_industryupdates_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='industryupdates',
            name='slug',
            field=models.SlugField(default='qdsmxog6ynzttbr01efn', verbose_name='Industry Slug'),
        ),
    ]
