# Generated by Django 3.1.11 on 2021-07-18 19:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0002_remove_city_state'),
    ]

    operations = [
        # migrations.AddField(
        #     model_name='city',
        #     name='state',
        #     field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='address.state', verbose_name='State'),
        # ),
    ]
