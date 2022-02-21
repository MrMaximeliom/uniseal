from django.db import models
from django.utils.translation import gettext_lazy as _

class ManageProductsPage(models.Model):
    objects = None
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.DO_NOTHING,
        verbose_name=_('User'),

    )
    product_page_views = models.PositiveIntegerField(
        verbose_name=_('Product Page Views'),
        default=1

    )
    visit_date = models.DateField(
        auto_now_add= True,
        null=True
    )



class ManageProducts(models.Model):
    product = models.ForeignKey(
        "product.Product",
        on_delete=models.DO_NOTHING,
        verbose_name=_('Product'),
        related_name='manage_product'

    )
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.DO_NOTHING,
        verbose_name=_('User'),
        related_name="manage_user_products"

    )
    product_views = models.PositiveIntegerField(
        verbose_name=_('Product Views'),
        blank=True,
        default=1
    )
    product_sheet_downloads = models.PositiveIntegerField(
        verbose_name=('Product Sheet Downloads'),
        blank=True,
        default=0

    )
    add_to_cart_views = models.PositiveIntegerField(
        verbose_name=_('Count of add to cart'),
        blank=True,
        default=0
    )

    class Meta:
        unique_together = ['product', 'user']

class ManageProjects(models.Model):
    project = models.ForeignKey(
        "project.Project",
        on_delete=models.DO_NOTHING,
        verbose_name=_('Project'),

    )
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.DO_NOTHING,
        verbose_name=_('User'),

    )
    project_views = models.PositiveIntegerField(
        verbose_name=_('Project Views'),
        default=1
    )

    class Meta:
        unique_together = ['project', 'user']

class ManageSolution(models.Model):
    solution = models.ForeignKey(
        "solution.Solution",
        on_delete=models.DO_NOTHING,
        verbose_name=_('Soltion'),

    )
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.DO_NOTHING,
        verbose_name=_('User'),

    )
    solution_views = models.PositiveIntegerField(
        verbose_name=_('Solution Views'),
        default=1
    )

    class Meta:
        unique_together = ['solution', 'user']

class ManageSellingPoints(models.Model):
    selling_point = models.ForeignKey(
        "sellingPoint.SellingPoint",
        on_delete=models.DO_NOTHING,
        verbose_name=_('Selling Point'),

    )
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.DO_NOTHING,
        verbose_name=_('User'),

    )
    phone_number_clicks = models.PositiveIntegerField(
        verbose_name=_('Phone Number Clicks'),
        default=0
    )
    secondary_phone_number = models.PositiveIntegerField(
        verbose_name=_('Secondary Phone Number Clicks'),
        default=0
    )

    class Meta:
        unique_together = ['user', 'selling_point']

class ManageBrochures(models.Model):
    brochures = models.ForeignKey(
        "brochures.Brochures",
        on_delete=models.DO_NOTHING,
        verbose_name=_('Brochure'),

    )
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.DO_NOTHING,
        verbose_name=_('User'),

    )
    brochures_views = models.PositiveIntegerField(
        verbose_name=_('Brochures_views'),
        default=1
    )
    brochures_sheet_downloads = models.PositiveIntegerField(
        verbose_name=('Brochures Sheet Downloads'),
        default=0
    )

    class Meta:
        unique_together = ['user', 'brochures']



class ManageCarts(models.Model):
    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.DO_NOTHING,
        verbose_name=_('Order'),

    )
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.DO_NOTHING,
        verbose_name=_('User'),

    )
    is_order_placed = models.BooleanField(
        default=False,

    )

    class Meta:
        unique_together = ['order', 'user']


