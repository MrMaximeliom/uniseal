from django.db import models
from django.utils import timezone
import string
import random
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Supplier(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_('Supplier Name')
    )
    image = models.ImageField(
        verbose_name=_('Supplier Image')
    )


class Product(models.Model):
    name = models.CharField(
        max_length=100, verbose_name=_('Product Name'))
    image = models.ImageField(
        upload_to='product_images/',
        verbose_name=_('Product Image'))
    category = models.CharField(
        max_length=150,
        verbose_name=_('Product Category')
    )
    product_file = models.FileField(
        upload_to='product_files/',
        null=True,
        blank=True,
        verbose_name=_('Product File'))
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('Product Description')
    )
    supplier_name = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        verbose_name=_('Supplier Name')
    )
    added_date = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('Added Date'))

    def __str__(self):
        return self.name


def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))


class ProductImages(models.Model):
    image = models.ImageField(
        upload_to="product_images",
        verbose_name=_('Product Image')
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_('Product')
    )


class ProductVideos(models.Model):
    video = models.URLField(
        verbose_name=_('Product Video Url')
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_('Product')
    )


class SimilarProduct(models.Model):
    original_product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_('Original Product')
    )
    similar_product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_('Similar Product'),
        related_name="similar_product"
    )

    def __str__(self):
        return self.original_product + 'similar to' + self.similar_product


class Project(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_('Project Name')
    )
    category = models.CharField(
        max_length=100,
        verbose_name=_('Product Category')
    )
    image = models.ImageField(
        upload_to='project_images',
        verbose_name=_('Project Image')
    )
    description = models.TextField(
        verbose_name=_('Project Description'),
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class ProjectImages(models.Model):
    image = models.ImageField(
        upload_to="project_images",
        verbose_name=_('Project Image')
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        verbose_name=_('Project')
    )


class ProjectVideos(models.Model):
    video = models.URLField(
        verbose_name=_('Project Video Url')
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        verbose_name=_('Project')
    )


class SellingPoint(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name=_('Sale Point Name')
    )
    image = models.ImageField(
        upload_to='sale_point_image',
        verbose_name=('Sale Point Image')
    )
    location = models.CharField(
        max_length=200,
        verbose_name=_('Sale Point Location')
    )
    address = models.CharField(
        max_length=250,
        verbose_name=_('Sale Point Address')
    )


class SellingPointsContactInfo(models.Model):
    primary_phone = models.CharField(
        max_length=20,
        verbose_name=_('Sale Point Primary Phone')
    )
    secondary_phone = models.CharField(
        max_length=20,
        verbose_name=_('Sale Point Secondary Phone')
    )


class Brochures(models.Model):
    name = models.CharField(
        max_length=120,
        verbose_name=_('Document Name')
    )
    image = models.ImageField(
        verbose_name=_('Document Image'),
        upload_to='document_image'
    )
