from django.db import models
from Util.ListsOfData import ORDER_STATUSES

class Order(models.Model):
    status = models.CharField(
        max_length=250,
        null=False,
        blank=False,
        choices=ORDER_STATUSES
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.pk)

class Cart(models.Model):
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name='user'    )
    product = models.ForeignKey(
        "product.Product",
        on_delete=models.CASCADE,
        related_name='product'
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order'
    )
    quantity = models.PositiveIntegerField(
        null=False,
        blank=False,
    )
