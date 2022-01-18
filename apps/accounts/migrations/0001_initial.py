# Generated by Django 3.1.11 on 2021-07-18 18:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('address', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=100, unique=True, verbose_name='Phone Number')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Email Address')),
                ('name', models.CharField(max_length=150, verbose_name='Name')),
                ('address', models.CharField(max_length=250, verbose_name='Address')),
                ('message', models.TextField(verbose_name='Message')),
                ('website', models.URLField(verbose_name='Website')),
                ('facebook', models.URLField(verbose_name='Facebook')),
                ('twitter', models.URLField(verbose_name='Twitter')),
                ('linkedin', models.URLField(verbose_name='LinkedIn')),
                ('instagram', models.URLField(verbose_name='Instagram')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('username', models.CharField(max_length=350, unique=True, verbose_name='User Name')),
                ('full_name', models.CharField(max_length=350, verbose_name='Full Name')),
                ('organization', models.CharField(max_length=350, verbose_name='Organization')),
                ('working_field', models.CharField(blank=True, choices=[('Civil Engineering', 'Civil Engineering'), ('Chemical Engineering', 'Chemical Engineering')], max_length=150, null=True, verbose_name='Working Field')),
                ('phone_number', models.CharField(max_length=100, unique=True, verbose_name='Phone Number')),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=10, verbose_name='Gender')),
                # ('city', models.CharField(blank=True, choices=[(1, 'Al-Khartoum'), (2, 'Bahry'), (3, 'Om-Durman')], max_length=10, null=True, verbose_name='City List')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Email Address')),
                ('is_active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('last_login', models.DateTimeField(auto_now=True, null=True)),
                ('registration_datetime', models.DateTimeField(auto_now_add=True, null=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='address.city', verbose_name='City')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]