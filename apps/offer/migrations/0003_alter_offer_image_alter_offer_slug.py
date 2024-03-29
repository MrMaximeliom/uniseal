# Generated by Django 4.0.1 on 2022-02-06 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0002_offer_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='image',
            field=models.ImageField(upload_to='offer_images', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='slug',
            field=models.SlugField(default='xbd7ignfvlswb250z2up', verbose_name='Offer Slug'),
        ),
    ]
