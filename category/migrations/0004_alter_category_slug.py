# Generated by Django 3.2.4 on 2021-08-02 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0003_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(default='b2vattsiont1hx7cqk91', verbose_name='Product Slug'),
        ),
    ]
