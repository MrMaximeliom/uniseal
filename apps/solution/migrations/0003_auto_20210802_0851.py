# Generated by Django 3.2.4 on 2021-08-02 08:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solution', '0002_auto_20210726_0727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solutionimages',
            name='solution',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='solution.solution', verbose_name='Solution'),
        ),
        migrations.AlterField(
            model_name='solutionvideos',
            name='solution',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='solution.solution', verbose_name='Solution'),
        ),
    ]
