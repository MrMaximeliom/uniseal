# Generated by Django 4.0 on 2022-02-21 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0019_rename_visit_date_time_manageproductspage_visit_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='managecarts',
            name='is_order_paced',
            field=models.BooleanField(default=False),
        ),
    ]
