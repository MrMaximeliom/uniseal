from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from apps.common_code.views import ModelListView, ModelDeleteView, UpdateModelView, AddModelView
from apps.industry_updates.models import IndustryUpdates

urlpatterns = [
    path('allUpdates', staff_member_required(ModelListView.as_view(
        model=IndustryUpdates,
        template_name="industry_updates/all_updates.html",
        main_active_flag="industry_updates",
        active_flag="all_updates",
        model_name="IndustryUpdates",
        title="All Industry Updates"
    ), login_url="login"), name="allUpdates"),
    path('addUpdates', staff_member_required(AddModelView.as_view(
        model=IndustryUpdates,
        fields=['headline','arabic_headline',
                'link','image_link','details','arabic_details','date'],
        main_active_flag="industry_updates",
        active_flag="add_updates",
        reference_field_name="headline",
        template_name="industry_updates/add_updates.html",
        title="Add Industry Updates",
        success_url="addUpdates"
    ), login_url="login"), name="addUpdates"),
    path('deleteUpdates', staff_member_required(ModelListView.as_view(
        model=IndustryUpdates,
        template_name="industry_updates/delete_updates.html",
        main_active_flag="industry_updates",
        active_flag="delete_updates",
        model_name="IndustryUpdates",
        title="Delete Industry Updates"
    ), login_url="login"), name="deleteUpdates"),
    path('deleteUpdate/<slug:slug>', staff_member_required(ModelDeleteView.as_view(
        model=IndustryUpdates,
        main_active_flag="industry_updates",
        active_flag="delete_updates",
        model_name='IndustryUpdates',
        title="Delete Industry Update",
        success_url="deleteUpdates"
    ), login_url="login"), name="deleteUpdate"),
    path('editUpdates', staff_member_required(ModelListView.as_view(
        model=IndustryUpdates,
        template_name="industry_updates/edit_updates.html",
        main_active_flag="industry_updates",
        active_flag="edit_updates",
        model_name="IndustryUpdates",
        title="Update Industry Updates"
    ), login_url="login"), name="editUpdates"),
    path('editUpdate/<slug:slug>', staff_member_required(UpdateModelView.as_view(
        model=IndustryUpdates,
        fields=['headline', 'arabic_headline',
                'link', 'image_link', 'details', 'arabic_details','date'],
        active_flag="edit_updates",
        main_active_flag="industry_updates",
        reference_field_name="headline",
        template_name="industry_updates/edit_update.html",
        title="Update Industry Updates",
        success_url="editUpdates"
    ), login_url="login"), name="editUpdate"),

    ]