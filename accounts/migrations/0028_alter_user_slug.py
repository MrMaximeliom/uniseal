# Generated by Django 4.0 on 2022-01-03 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0027_alter_contactus_id_alter_user_id_alter_user_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='slug',
            field=models.SlugField(default='0lt3t2smaua5d4vpkvjb', verbose_name='User Slug'),
        ),
    ]
