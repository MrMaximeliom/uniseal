# Generated by Django 4.0.1 on 2022-02-01 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0040_alter_user_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='slug',
            field=models.SlugField(default='b4egzi7jk1ptbshpl3fi', verbose_name='User Slug'),
        ),
    ]
