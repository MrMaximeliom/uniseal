# Generated by Django 4.0.1 on 2022-02-05 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0028_alter_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(default='fozbuzlkdvrgj7ict0hv', verbose_name='Product Slug'),
        ),
    ]
