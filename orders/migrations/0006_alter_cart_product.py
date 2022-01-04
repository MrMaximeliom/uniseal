# Generated by Django 4.0 on 2022-01-04 09:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0039_alter_product_slug'),
        ('orders', '0005_alter_cart_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_details', to='product.product'),
        ),
    ]
