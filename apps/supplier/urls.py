from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from apps.common_code.views import ModelDeleteView, AddModelView, UpdateModelView
from apps.supplier.dahsboard_views import SuppliersListView
from apps.supplier.models import Supplier

urlpatterns = [
    path('allSuppliers', staff_member_required(SuppliersListView.as_view(
        model=Supplier,
        template_name="supplier/all_suppliers.html",
        main_active_flag="suppliers",
        active_flag="all_suppliers",
        model_name="Supplier",
        title="All Suppliers"
    ), login_url="login"), name="allSuppliers"),
    path('addSuppliers', staff_member_required(AddModelView.as_view(
        model=Supplier,
        fields=['name', 'arabic_name',
                'image', 'link'],
        main_active_flag="suppliers",
        active_flag="add_suppliers",
        reference_field_name="name",
        template_name="supplier/add_suppliers.html",
        title="Add Suppliers",
        success_url="allSuppliers"
    ), login_url="login"), name="addSuppliers"),
    path('deleteSuppliers', staff_member_required(SuppliersListView.as_view(
        model=Supplier,
        template_name="supplier/delete_suppliers.html",
        main_active_flag="suppliers",
        active_flag="delete_suppliers",
        model_name="Supplier",
        title="Delete Suppliers"
    ), login_url="login"), name="deleteSuppliers"),
    path('deleteSupplier/<slug:slug>', staff_member_required(ModelDeleteView.as_view(
        model=Supplier,
        main_active_flag="suppliers",
        active_flag="delete_suppliers",
        model_name='Supplier',
        title="Delete Suppliers",
        success_url="deleteSuppliers"
    ), login_url="login"), name="deleteSupplier"),
    path('editSuppliers', staff_member_required(SuppliersListView.as_view(
        model=Supplier,
        template_name="supplier/edit_suppliers.html",
        main_active_flag="suppliers",
        active_flag="edit_suppliers",
        model_name="Supplier",
        title="Edit Suppliers"
    ), login_url="login"), name="editSuppliers"),
    path('editSupplier/<str:slug>', staff_member_required(UpdateModelView.as_view(
        model=Supplier,
        fields=['name', 'arabic_name',
                'image', 'link'],
        main_active_flag="suppliers",
        active_flag="edit_suppliers",
        reference_field_name="name",
        template_name="supplier/edit_supplier.html",
        title="Edit Suppliers",
        success_url="allSuppliers"
    ), login_url="login"), name="editSupplier"),

    ]