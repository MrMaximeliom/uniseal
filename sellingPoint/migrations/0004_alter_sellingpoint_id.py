# Generated by Django 3.2.4 on 2021-07-04 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellingPoint', '0003_auto_20210629_1856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellingpoint',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
