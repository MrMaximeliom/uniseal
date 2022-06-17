from django.db import models
from django.template.defaultfilters import slugify  # new
from django.urls import reverse_lazy
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
    price = models.FloatField(
        verbose_name=_('Price'),
        null=True,
        blank=False,
        default="0.0"

    )
    discount_percentage = models.FloatField(
        verbose_name=_('Discount Percentage'),
        null=True,
        blank=True,
        default=0.0
    )


    def __str__(self):
        return self.name

    # return not wanted fields' names in the process of creating new report file from this model
    def get_not_wanted_fields_names_in_report_file(self=None):
        return ["id", "slug","arabic_name","image","product_file",
                "arabic_description","video","is_top","discount_percentage"]

    def save(self, *args, **kwargs): # new+
        if not self.slug:
            self.slug = slugify(rand_slug()+ "-" +self.name)
        return super().save(*args, **kwargs)



    def get_absolute_url(self):
        return reverse_lazy("allProducts")




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

    def save(self, *args, **kwargs):
        from datetime import datetime
        self.slug = slugify(rand_slug() + "-" + "-" + str(datetime.now().second))
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy("productImages-dash")


class ProductVideos(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Product')
    )

    def save(self, *args, **kwargs):
        from datetime import datetime
        self.slug = slugify(rand_slug() + "-" + "-" + str(datetime.now().second))
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy("productImages-dash")


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

    def get_absolute_url(self):
        return reverse_lazy("allProducts")

