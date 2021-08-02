from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
# Create your models here.
from Util.utils import rand_slug


class CompanyInfo(models.Model):
    from django.core.validators import RegexValidator
    phone_regex = RegexValidator(regex=r'^9\d{8}$|^1\d{8}$',
                                 message=_("Phone number must start with 9 or 1 (no zeros) and includes 9 numbers."))

    phone_number = models.CharField(
        verbose_name=_('Company Primary Phone Number'),
        blank=False,
        null=False,
        max_length=100,
        unique=True
    )

    email = models.EmailField(
        verbose_name=_('Company Email Address'),
        max_length=255,
        unique=True,

    )
    company_name = models.CharField(
        max_length=150,
        verbose_name=_('Company Name'),
        blank=False,
        null=False,

    )
    main_address = models.CharField(
        max_length=250,
        verbose_name=_('Company Main Address'),
        blank=False,
        null=False,

    )
    country = models.ForeignKey(
        "address.Country",
        verbose_name=_('Country'),
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    state= models.ForeignKey(
        "address.State",
        verbose_name=_('State'),
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    city = models.ForeignKey(
        "address.City",
        verbose_name=_('City'),
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    website = models.URLField(
        verbose_name=_('Website'),
        blank = True,
        null = True
    )
    facebook = models.URLField(
        verbose_name=_('Facebook'),
        blank=True,
        null=True
    )
    twitter = models.URLField(
        verbose_name=_('Twitter'),
        blank=True,
        null=True
    )
    linkedin = models.URLField(
        verbose_name=_('LinkedIn'),
        blank=True,
        null=True
    )
    instagram = models.URLField(
        verbose_name=_('Instagram'),
        blank=True,
        null=True
    )
    slug = models.SlugField(
        default=slugify(rand_slug()),
        verbose_name=_('Company Slug')

    )

    def __str__(self):
        return self.company_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(rand_slug() + "-" + str(self.company_name))
        return super().save(*args, **kwargs)