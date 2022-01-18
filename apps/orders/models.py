from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
from Util.ListsOfData import ORDER_STATUSES
from Util.utils import random_order_id
class Order(models.Model):
    slug = models.SlugField(
        default=slugify(random_order_id(5, 4)),
        verbose_name=_('Token Slug'),
    )
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name='user')
    status = models.CharField(
        max_length=250,
        null=False,
        blank=False,
        choices=ORDER_STATUSES
    )
    total = models.FloatField(
        default=0.0
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.pk)

class Cart(models.Model):

    product = models.ForeignKey(
        "product.Product",
        on_delete=models.CASCADE,
        related_name='product_details'
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_details'
    )
    quantity = models.PositiveIntegerField(
        null=False,
        blank=False,
    )

    def __str__(self):
        return 'product: '+self.product.name+' quantity: '+str(self.quantity)
