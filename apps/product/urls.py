from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from apps.common_code.views import ModelDeleteView, AddModelView, UpdateModelView
from apps.product import dashboard_views as product_views
from apps.product.dashboard_views import ProductListView
from apps.product.models import Product

urlpatterns = [
    path('allProducts', staff_member_required(ProductListView.as_view(
        model=Product,
        template_name="product/all_products.html",
        main_active_flag="products",
        active_flag="all_products",
        model_name="Product",
        title="All Products"
    ), login_url="login"), name="allProducts"),
    path('topProducts', product_views.top_products, name='topProducts'),
    path('addProducts', staff_member_required(AddModelView.as_view(
        model=Product,
        fields=['name','arabic_name',
                'image','category','product_file',
                'description','arabic_description',
                'supplier','video','is_top','price'
                ,'discount_percentage'],
        main_active_flag="products",
        active_flag="add_products",
        reference_field_name="name",
        template_name="product/add_products.html",
        title="Add Products",
        success_url="allProducts"
    ), login_url="login"), name="addProducts"),
    path('deleteProducts', staff_member_required(ProductListView.as_view(
        model=Product,
        template_name="product/delete_products.html",
        main_active_flag="products",
        active_flag="delete_products",
        model_name="Product",
        title="Delete Products"
    ), login_url="login"), name="deleteProducts"),
    path('deleteProduct/<str:slug>', staff_member_required(ModelDeleteView.as_view(
        model=Product,
        main_active_flag="products",
        active_flag="delete_products",
        model_name='Product',
        title="Delete Products",
        success_url="deleteProducts"
    ), login_url="login"), name="deleteProduct"),
    path('editProduct/<str:slug>', staff_member_required(UpdateModelView.as_view(
        model=Product,
        fields=['name', 'arabic_name',
                'image', 'category', 'product_file',
                'description', 'arabic_description',
                'supplier', 'video', 'is_top', 'price'
            , 'discount_percentage'],
        main_active_flag="products",
        active_flag="edit_products",
        reference_field_name="name",
        template_name="product/edit_product.html",
        title="Edit Products",
        success_url="allProducts"
    ), login_url="login"), name="editProduct"),
    path('editProducts', staff_member_required(ProductListView.as_view(
        model=Product,
        template_name="product/edit_products.html",
        main_active_flag="products",
        active_flag="edit_products",
        model_name="Product",
        title="Edit Products"
    ), login_url="login"), name="editProducts"),
    path('productDetails/<str:slug>', product_views.product_details, name='productDetails'),
    path('productImages/<str:slug>', product_views.product_images, name='productImages'),
    path('productImages/', product_views.product_images, name='productImages-dash')
    ]
