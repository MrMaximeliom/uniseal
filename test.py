from apps.admin_panel.models import ManageProducts
from apps.product.models import Product
from django.db.models import Count
if __name__ == "__main__":
    viewed_products = ManageProducts.objects.values("product").annotate(users_count=Count('user'))
    for product in viewed_products:
        print(product)
