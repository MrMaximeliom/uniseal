# Generated by Django 4.0.2 on 2022-02-19 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0016_alter_managebrochures_brochures_views_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='manageproductspage',
            name='visit_date_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]