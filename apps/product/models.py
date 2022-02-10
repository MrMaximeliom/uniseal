from django.db import models
from django.template.defaultfilters import slugify  # new
from django.utils.translation import gettext_lazy as _

from Util.utils import rand_slug


class Product(models.Model):
    name = models.CharField(
        max_length=100, verbose_name=_('Product Name'))
    arabic_name = models.CharField(
        max_length=100,
        verbose_name=_('Product Name(Arabic)'),
    null=True,
        blank=True
    )
    image = models.ImageField(
        upload_to='product_images/',
        verbose_name=_('Product Image'))
    category = models.ForeignKey(
    "category.Category",
        on_delete=models.SET_NULL,
        null=True,
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
    arabic_description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('Product Description(Arabic)')
    )
    supplier = models.ForeignKey(
        "supplier.Supplier",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Supplier Name')
    )
    added_date = models.DateField(
       auto_now= True,
        verbose_name=_('Added Date'))
    slug = models.SlugField(
        default=slugify(rand_slug()),
        verbose_name=_('Product Slug')

    )
    video = models.URLField(
        verbose_name=_('Product Video Url'),
        blank=True,
        null=True

    )
    is_top = models.BooleanField(
        verbose_name=_('Is Top Product?'),
        default=False
    )
    price = models.DecimalField(
        verbose_name=_('Price'),
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=False,

    )
    discount_percentage = models.DecimalField(
        verbose_name=_('Discount Percentage'),
        max_digits=19,
        decimal_places=10,
        null=True,
        blank=False,
    )


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs): # new+
        if not self.slug:
            self.slug = slugify(rand_slug()+ "-" +self.name)
        return super().save(*args, **kwargs)




class ProductImages(models.Model):
    image = models.ImageField(
        upload_to="product_images",
        verbose_name=_('Product Image')
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        null=True,
        verbose_name=_('Product')
    )


class ProductVideos(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Product')
    )


class SimilarProduct(models.Model):
    original_product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Original Product')
    )
    similar_product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Similar Product'),
        related_name="similar_product"
    )

    def __str__(self):
        return self.original_product + 'similar to' + self.similar_product

