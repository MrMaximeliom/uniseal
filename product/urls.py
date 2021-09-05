from django.urls import path
from product import views as product_views
urlpatterns = [
    path('allProducts', product_views.all_products, name='allProducts'),
    path('addProducts', product_views.add_products, name='addProducts'),
    path('deleteProducts', product_views.delete_products, name='deleteProducts'),
    path('editProduct/<str:slug>', product_views.edit_product, name='editProduct'),
    path('editProducts', product_views.edit_products, name='editProducts'),
    path('productDetails/<str:slug>', product_views.product_details, name='productDetails'),
    path('productImages/<str:slug>', product_views.product_images, name='productImages'),
    path('productImages/', product_views.product_images, name='productImages-dash'),
    path('confirmDelete/<int:id>', product_views.confirm_delete, name='productDelete'),]