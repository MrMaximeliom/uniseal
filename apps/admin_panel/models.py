from django.db import models
from django.utils.translation import gettext_lazy as _

class ManageProductsPage(models.Model):
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        verbose_name=_('User'),
        null=True,
        blank=False,
    )
    product_page_views = models.PositiveIntegerField(
        verbose_name=_('Product Page Views'),
    )



class ManageProducts(models.Model):
    product = models.ForeignKey(
        "product.Product",
        on_delete=models.SET_NULL,
        verbose_name=_('Product'),
        null=True,
        blank=False,
    )
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        verbose_name=_('User'),
        null=True,
        blank=False,
    )
    product_views = models.PositiveIntegerField(
        verbose_name=_('Product Views'),
    )
    product_sheet_downloads = models.PositiveIntegerField(
        verbose_name=('Product Sheet Downloads')
    )

class ManageProjects(models.Model):
    project = models.ForeignKey(
        "project.Project",
        on_delete=models.SET_NULL,
        verbose_name=_('Project'),
        null=True,
        blank=False,
    )
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        verbose_name=_('User'),
        null=True,
        blank=False,
    )
    project_views = models.PositiveIntegerField(
        verbose_name=_('Project Views'),
    )

class ManageSolution(models.Model):
    solution = models.ForeignKey(
        "solution.Solution",
        on_delete=models.SET_NULL,
        verbose_name=_('Soltion'),
        null=True,
        blank=False,
    )
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        verbose_name=_('User'),
        null=True,
        blank=False,
    )
    solution_views = models.PositiveIntegerField(
        verbose_name=_('Solution Views'),
    )

class ManageSellingPoints(models.Model):
    selling_point = models.ForeignKey(
        "sellingPoint.SellingPoint",
        on_delete=models.SET_NULL,
        verbose_name=_('Selling Point'),
        null=True,
        blank=False,
    )
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        verbose_name=_('User'),
        null=True,
        blank=False,
    )
    phone_number_clicks = models.PositiveIntegerField(
        verbose_name=_('Phone Number Clicks'),
    )
    secondary_phone_number = models.PositiveIntegerField(
        verbose_name=_('Secondary Phone Number Clicks'),
    )

class ManageBrochures(models.Model):
    brochures = models.ForeignKey(
        "brochures.Brochures",
        on_delete=models.SET_NULL,
        verbose_name=_('Brochure'),
        null=True,
        blank=False,
    )
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        verbose_name=_('User'),
        null=True,
        blank=False,
    )
    brochures_views = models.PositiveIntegerField(
        verbose_name=_('Brochures_views'),
    )
    brochures_sheet_downloads = models.PositiveIntegerField(
        verbose_name=('Brochures Sheet Downloads')
    )

class ManageCarts(models.Model):
    cart = models.ForeignKey(
        "orders.Cart",
        on_delete=models.SET_NULL,
        verbose_name=_('Carts'),
        null=True,
        blank=False,
    )
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        verbose_name=_('User'),
        null=True,
        blank=False,
    )
    add_to_cart_views = models.PositiveIntegerField(
        verbose_name=_('Add To Cart Views'),
    )

