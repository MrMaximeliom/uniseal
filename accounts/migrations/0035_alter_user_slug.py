# Generated by Django 4.0 on 2022-01-06 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0034_alter_user_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='slug',
            field=models.SlugField(default='btvkua2mpf8s8firnbwy', verbose_name='User Slug'),
        ),
    ]