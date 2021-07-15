# Generated by Django 3.1.11 on 2021-07-15 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellingPoint', '0004_alter_sellingpoint_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellingpoint',
            name='email',
            field=models.EmailField(blank=True, max_length=255, null=True, unique=True, verbose_name='Email Address'),
        ),
        migrations.AlterField(
            model_name='sellingpoint',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]