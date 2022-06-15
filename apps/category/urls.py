from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from apps.category.dashboard_views import CategoryListView
from apps.category.models import Category
from apps.common_code.views import UpdateModelView, ModelDeleteView, AddModelView

urlpatterns = [
    path('allCategories', staff_member_required(CategoryListView.as_view(
        model=Category,
        template_name="category/all_categories.html",
        main_active_flag="categories",
        active_flag="all_categories",
        model_name="Category",
        title="All Categories"
    ), login_url="login"), name="allCategories"),
    path('addCategories', staff_member_required(AddModelView.as_view(
        model=Category,
        fields=['name','arabic_name'],
        main_active_flag="categories",
        active_flag="add_categories",
        reference_field_name="name",
        template_name="category/add_categories.html",
        title="Add Categories",
        success_url="allCategories"
    ), login_url="login"), name="addCategories"),
    path('deleteCategories', staff_member_required(CategoryListView.as_view(
        model=Category,
        template_name="category/delete_categories.html",
        main_active_flag="categories",
        active_flag="delete_categories",
        model_name="Category",
        title="Delete Categories"
    ), login_url="login"), name="deleteCategories"),
    path('deleteCategory/<slug:slug>', staff_member_required(ModelDeleteView.as_view(
        model=Category,
        main_active_flag="categories",
        active_flag="delete_categories",
        model_name='Category',
        title="Delete Categories",
        success_url="deleteCategories"
    ), login_url="login"), name="deleteCategory"),
    path('editCategories', staff_member_required(CategoryListView.as_view(
        model=Category,
        template_name="category/edit_categories.html",
        main_active_flag="categories",
        active_flag="edit_categories",
        model_name="Category",
        title="Update Categories"
    ), login_url="login"), name="editCategories"),
    path('editCategory/<slug:slug>', staff_member_required(UpdateModelView.as_view(
        model=Category,
        fields=['name','arabic_name'],
        active_flag="edit_categories",
        main_active_flag="categories",
        reference_field_name="name",
        template_name="category/edit_category.html",
        title="Update Category",
        success_url="editCategories"
    ), login_url="login"), name="editCategory"),
    ]