# Generated by Django 3.1.11 on 2021-07-15 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brochures', '0005_brochures_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brochures',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
