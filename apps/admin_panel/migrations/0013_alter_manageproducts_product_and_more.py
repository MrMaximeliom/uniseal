# Generated by Django 4.0.2 on 2022-02-12 11:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0066_alter_product_slug'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('admin_panel', '0012_remove_managecarts_cart_managecarts_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manageproducts',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='manage_product', to='product.product', verbose_name='Product'),
        ),
        migrations.AlterField(
            model_name='manageproducts',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='manage_user_products', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
