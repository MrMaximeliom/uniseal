# Generated by Django 3.1.11 on 2021-07-17 19:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0002_auto_20210715_2232'),
        ('accounts', '0009_user_city_country'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='city',
        ),
        # migrations.AddField(
        #     model_name='user',
        #     name='city_country',
        #     field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='address.city', verbose_name='City'),
        #     preserve_default=False,
        # ),
    ]
