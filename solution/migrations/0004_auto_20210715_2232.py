# Generated by Django 3.1.11 on 2021-07-15 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solution', '0003_auto_20210704_0717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solution',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='solutionimages',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='solutionvideos',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]