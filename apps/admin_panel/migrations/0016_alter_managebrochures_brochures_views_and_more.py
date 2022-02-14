# Generated by Django 4.0 on 2022-02-14 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0015_alter_managebrochures_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='managebrochures',
            name='brochures_views',
            field=models.PositiveIntegerField(default=1, verbose_name='Brochures_views'),
        ),
        migrations.AlterField(
            model_name='manageproducts',
            name='product_views',
            field=models.PositiveIntegerField(blank=True, default=1, verbose_name='Product Views'),
        ),
        migrations.AlterField(
            model_name='manageproductspage',
            name='product_page_views',
            field=models.PositiveIntegerField(default=1, verbose_name='Product Page Views'),
        ),
        migrations.AlterField(
            model_name='manageprojects',
            name='project_views',
            field=models.PositiveIntegerField(default=1, verbose_name='Project Views'),
        ),
        migrations.AlterField(
            model_name='managesolution',
            name='solution_views',
            field=models.PositiveIntegerField(default=1, verbose_name='Solution Views'),
        ),
    ]
