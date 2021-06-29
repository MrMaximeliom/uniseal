from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import string
import random

class Product(models.Model):
    name = models.CharField(
        max_length=100, verbose_name=_('Product Name'))
    image = models.ImageField(
        upload_to='product_images/',
        verbose_name=_('Product Image'))
    category = models.ForeignKey(
    "category.Category",
        on_delete=models.CASCADE,
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
    supplier = models.ForeignKey(
        "supplier.Supplier",
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

