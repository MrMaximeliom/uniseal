from django.urls import path

from supplier import dahsboard_views as supplier_views

urlpatterns = [
    path('allSuppliers', supplier_views.all_suppliers, name='allSuppliers'),
    path('addSuppliers', supplier_views.add_suppliers, name='addSuppliers'),
    path('deleteSuppliers', supplier_views.delete_suppliers, name='deleteSuppliers'),
    path('deleteSupplier/<int:id>', supplier_views.confirm_delete, name='deleteSupplier'),
    path('editSuppliers', supplier_views.edit_suppliers, name='editSuppliers'),
    path('editSupplier/<str:slug>', supplier_views.edit_supplier, name='editSupplier'),

    ]