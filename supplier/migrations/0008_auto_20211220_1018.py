# Generated by Django 3.1.11 on 2021-12-20 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0007_auto_20211220_0956'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='arabic_name',
            field=models.CharField(max_length=100, null=True, verbose_name='Supplier Name(Arabic)'),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='slug',
            field=models.SlugField(default='10g7kbrnrij4jzdquek9', verbose_name='Supplier Slug'),
        ),
    ]