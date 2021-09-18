from django.urls import path

from category import dashboard_views as category_views

urlpatterns = [
    path('allCategories', category_views.all_categories, name='allCategories'),
    path('addCategories', category_views.add_categories, name='addCategories'),
    path('deleteCategories', category_views.delete_categories, name='deleteCategories'),
    path('editCategories', category_views.edit_categories, name='editCategories'),
    path('editCategory/<str:slug>', category_views.edit_category, name='editCategory'),
    path('deleteCategory/<int:id>', category_views.confirm_delete, name='deleteCategory'),

    ]