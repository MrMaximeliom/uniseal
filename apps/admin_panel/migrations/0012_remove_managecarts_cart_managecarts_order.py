# Generated by Django 4.0.2 on 2022-02-12 08:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0026_alter_order_slug'),
        ('admin_panel', '0011_alter_managebrochures_brochures_sheet_downloads_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='managecarts',
            name='cart',
        ),
        migrations.AddField(
            model_name='managecarts',
            name='order',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='orders.order', verbose_name='Order'),
            preserve_default=False,
        ),
    ]
