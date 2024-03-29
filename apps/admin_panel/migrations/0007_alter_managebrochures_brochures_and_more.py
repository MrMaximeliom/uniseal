# Generated by Django 4.0.1 on 2022-02-05 07:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0017_alter_order_slug'),
        ('product', '0050_alter_product_slug'),
        ('project', '0055_alter_application_slug_alter_project_slug'),
        ('brochures', '0030_alter_brochures_slug'),
        ('solution', '0006_alter_solution_id_alter_solutionimages_id_and_more'),
        ('sellingPoint', '0030_alter_sellingpoint_slug'),
        ('admin_panel', '0006_alter_managebrochures_id_alter_manageproducts_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='managebrochures',
            name='brochures',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='brochures.brochures', verbose_name='Brochure'),
        ),
        migrations.AlterField(
            model_name='managebrochures',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AlterField(
            model_name='manageproducts',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.product', verbose_name='Product'),
        ),
        migrations.AlterField(
            model_name='manageproducts',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AlterField(
            model_name='manageprojects',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='project.project', verbose_name='Project'),
        ),
        migrations.AlterField(
            model_name='manageprojects',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AlterField(
            model_name='managesellingpoints',
            name='selling_point',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sellingPoint.sellingpoint', verbose_name='Selling Point'),
        ),
        migrations.AlterField(
            model_name='managesellingpoints',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AlterField(
            model_name='managesolution',
            name='solution',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='solution.solution', verbose_name='Soltion'),
        ),
        migrations.AlterField(
            model_name='managesolution',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.CreateModel(
            name='ManageCarts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_to_cart_views', models.PositiveIntegerField(verbose_name='Add To Cart Views')),
                ('cart', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.cart', verbose_name='Carts')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
    ]
