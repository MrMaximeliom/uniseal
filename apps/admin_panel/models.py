from django.db import models
from django.utils.translation import gettext_lazy as _


class ManageProducts(models.Model):
    product = models.ForeignKey(
        "product.Product",
        on_delete=models.CASCADE,
        verbose_name=_('Product')
    )
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        verbose_name=_('User'),
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
        on_delete=models.CASCADE,
        verbose_name=_('Project')
    )
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        verbose_name=_('User'),
    )
    project_views = models.PositiveIntegerField(
        verbose_name=_('Project Views'),
    )

class ManageSolution(models.Model):
    solution = models.ForeignKey(
        "solution.Solution",
        on_delete=models.CASCADE,
        verbose_name=_('Soltion')
    )
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        verbose_name=_('User'),
    )
    solution_views = models.PositiveIntegerField(
        verbose_name=_('Solution Views'),
    )

class ManageSellingPoints(models.Model):
    selling_point = models.ForeignKey(
        "sellingPoint.SellingPoint",
        on_delete=models.CASCADE,
        verbose_name=_('Selling Point')
    )
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        verbose_name=_('User'),
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
        on_delete=models.CASCADE,
        verbose_name=_('Brochures')
    )
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        verbose_name=_('User'),
    )
    brochures_views = models.PositiveIntegerField(
        verbose_name=_('Brochures_views'),
    )
    brochures_sheet_downloads = models.PositiveIntegerField(
        verbose_name=('Brochures Sheet Downloads')
    )
