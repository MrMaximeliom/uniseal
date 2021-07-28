# Generated by Django 3.2.4 on 2021-07-28 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_auto_20210728_0723'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, verbose_name='Project Application')),
            ],
        ),
        # migrations.AlterField(
        #     model_name='project',
        #     name='slug',
        #     field=models.SlugField(default='0el43z', verbose_name='Project Slug'),
        # ),
        # migrations.AddField(
        #     model_name='project',
        #     name='application',
        #     field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='project.application', verbose_name='Application'),
        #     preserve_default=False,
        # ),
    ]
