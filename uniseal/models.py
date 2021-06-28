from django.db import models
from django.utils import timezone
import string
import random
from django.utils.translation import gettext_lazy as _

class Supplier(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_('Supplier Name')
    )
    image = models.ImageField(
        verbose_name=_('Supplier Image')
    )


class Category(models.Model):
    name = models.CharField(
        verbose_name=_('Category Name'),
        max_length=150
    )


class Product(models.Model):
    name = models.CharField(
        max_length=100, verbose_name=_('Product Name'))
    image = models.ImageField(
        upload_to='product_images/',
        verbose_name=_('Product Image'))
    category = models.ForeignKey(
        Category,
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
    title = models.CharField(
        max_length=120,
        verbose_name=_('Project Title')
    )
    category = models.CharField(
        max_length=100,
        verbose_name=_('Project Category')
    )
    beneficiary = models.CharField(
        max_length=100,
        verbose_name=_('Project Beneficiary')
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


class Solution(models.Model):
    title = models.CharField(
        verbose_name=_('Solution Title'),
        max_length=150
    )
    description = models.TextField(
        verbose_name=_('Solution Description'),
        null=True,
        blank=True
    )


class SolutionImages(models.Model):
    image = models.ImageField(
        upload_to="solution_images",
        verbose_name=_('Solution Image')
    )
    solution = models.ForeignKey(
        Solution,
        on_delete=models.CASCADE,
        verbose_name=_('Solution')
    )


class SolutionVideos(models.Model):
    video = models.URLField(
        verbose_name=_('Solution Video Url')
    )
    solution = models.ForeignKey(
        Solution,
        on_delete=models.CASCADE,
        verbose_name=_('Solution')
    )


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
    from Util.ListsOfData import CITIES_CHOICES, AREA_CHOICES
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
    city = models.CharField(
        verbose_name=_('City'),
        blank=False,
        null=False,
        choices=CITIES_CHOICES,
        max_length=350,
        default=1
    )
    area = models.CharField(
        verbose_name=_("Area"),
        blank=False,
        null=False,
        choices=AREA_CHOICES,
        max_length=300,
        default=1
    )
    phone_number = models.CharField(
        verbose_name=_('Phone Number'),
        blank=False,
        null=False,
        max_length=100,
        unique=True
    )
    email = models.EmailField(
        verbose_name=_('Email Address'),
        max_length=255,
        unique=True,
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
    title = models.CharField(
        max_length=120,
        verbose_name=_('Document Title')
    )
    attachment = models.FileField(
        verbose_name=_('Document Attachment'),
        upload_to='document_field'
    )

class ContactUs(models.Model):
    from Util.ListsOfData import CITIES_CHOICES, AREA_CHOICES
    from django.core.validators import RegexValidator
    phone_regex = RegexValidator(regex=r'^9\d{8}$|^1\d{8}$',
                                 message=_("Phone number must start with 9 or 1 (no zeros) and includes 9 numbers."))

    phone_number = models.CharField(
        verbose_name=_('Phone Number'),
        blank=False,
        null=False,
        max_length=100,
        unique=True
    )

    email = models.EmailField(
        verbose_name=_('Email Address'),
        max_length=255,
        unique=True,
    )
    name = models.CharField(
        max_length=150,
        verbose_name=_('Name')
    )
    address = models.CharField(
        max_length=250,
        verbose_name=_('Address')
    )
    message = models.TextField(
        verbose_name=_('Message'),
    )
    website = models.URLField(
        verbose_name=_('Website')
    )
    facebook = models.URLField(
        verbose_name=_('Facebook')
    )
    twitter = models.URLField(
        verbose_name=_('Twitter')
    )
    linkedin = models.URLField(
        verbose_name=_('LinkedIn')
    )
    instagram = models.URLField(
        verbose_name=_('Instagram')
    )



