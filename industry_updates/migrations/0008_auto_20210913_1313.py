# Generated by Django 3.1.11 on 2021-09-13 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('industry_updates', '0007_auto_20210904_0806'),
    ]

    operations = [
        migrations.AddField(
            model_name='industryupdates',
            name='date',
            field=models.DateField(default='2021-09-12', verbose_name='Date'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='industryupdates',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='industryupdates',
            name='slug',
            field=models.SlugField(default='53q0gdrcpynesdp5c1lw', verbose_name='Industry Slug'),
        ),
    ]
