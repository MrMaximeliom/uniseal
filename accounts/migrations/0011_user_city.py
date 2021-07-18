# Generated by Django 3.1.11 on 2021-07-17 19:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [

        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='address.city', verbose_name='City'),
            preserve_default=False,
        ),
        # migrations.AlterField(
        #     model_name='user',
        #     name='city',
        #     field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        # ),
    ]
