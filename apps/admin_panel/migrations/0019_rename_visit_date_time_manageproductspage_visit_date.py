# Generated by Django 4.0 on 2022-02-20 08:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0018_alter_manageproductspage_visit_date_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='manageproductspage',
            old_name='visit_date_time',
            new_name='visit_date',
        ),
    ]
