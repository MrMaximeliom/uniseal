# Generated by Django 3.1.11 on 2021-07-21 08:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0004_remove_city_country'),
        ('sellingPoint', '0004_auto_20210718_2119'),
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
        # migrations.AddField(
        #     model_name='sellingpoint',
        #     name='area',
        #     field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='address.area'),
        # ),
        # migrations.AddField(
        #     model_name='sellingpoint',
        #     name='city',
        #     field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='address.city'),
        # ),
        # migrations.AddField(
        #     model_name='sellingpoint',
        #     name='country',
        #     field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='address.country'),
        # ),
        # migrations.AddField(
        #     model_name='sellingpoint',
        #     name='state',
        #     field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='address.state'),
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
