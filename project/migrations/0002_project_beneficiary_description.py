# Generated by Django 3.1.11 on 2021-07-21 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='beneficiary_description',
            field=models.TextField(blank=True, null=True, verbose_name='Beneficiary Description'),
        ),
    ]