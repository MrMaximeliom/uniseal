# Generated by Django 3.2.5 on 2021-07-30 20:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0013_auto_20210730_2006'),
        ('sellingPoint', '0004_auto_20210728_0642'),
    ]

    operations = [
        # migrations.RemoveField(
        #     model_name='productimages',
        #     name='product',
        # ),
        # migrations.RemoveField(
        #     model_name='productvideos',
        #     name='product',
        # ),
        # migrations.RemoveField(
        #     model_name='similarproduct',
        #     name='original_product',
        # ),
        # migrations.RemoveField(
        #     model_name='similarproduct',
        #     name='similar_product',
        # ),
        migrations.AddField(
            model_name='sellingpoint',
            name='area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='address.area'),
        ),
        migrations.AddField(
            model_name='sellingpoint',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='address.city'),
        ),
        migrations.AddField(
            model_name='sellingpoint',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='address.country'),
        ),
        migrations.AddField(
            model_name='sellingpoint',
            name='slug',
            field=models.SlugField(default='nqufkp', verbose_name='Selling Point Slug'),
        ),
        migrations.AddField(
            model_name='sellingpoint',
            name='state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='address.state'),
        ),
        # migrations.AlterField(
        #     model_name='sellingpoint',
        #     name='email',
        #     field=models.EmailField(default='', max_length=255, unique=True, verbose_name='Email Address'),
        #     preserve_default=False,
        # ),
        # migrations.AlterField(
        #     model_name='sellingpoint',
        #     name='id',
        #     field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        # ),
        # migrations.DeleteModel(
        #     name='Product',
        # ),
        # migrations.DeleteModel(
        #     name='ProductImages',
        # ),
        # migrations.DeleteModel(
        #     name='ProductVideos',
        # ),
        # migrations.DeleteModel(
        #     name='SimilarProduct',
        # ),
    ]