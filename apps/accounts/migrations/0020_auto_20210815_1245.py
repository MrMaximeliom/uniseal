# Generated by Django 3.2.4 on 2021-08-15 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_alter_user_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactus',
            name='marketing_executive_phone_number',
            field=models.CharField(default='', max_length=100, unique=True, verbose_name='Marketing Executive Phone Number'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='slug',
            field=models.SlugField(default='4on74ghllkeqkhe4chkt', verbose_name='User Slug'),
        ),
    ]