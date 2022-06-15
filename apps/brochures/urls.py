from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from apps.brochures.models import Brochures
from apps.common_code.views import ModelDeleteView, ModelListView, UpdateModelView, AddModelView

urlpatterns = [
    path('allBrochures', staff_member_required(ModelListView.as_view(
        model=Brochures,
        template_name="brochures/all_brochures.html",
        main_active_flag="brochures",
        active_flag="all_brochures",
        model_name="Brochures",
        title="All Brochures"
    ), login_url="login"), name="allBrochures"),
    path('addBrochures', staff_member_required(AddModelView.as_view(
        model=Brochures,
        fields=['title','arabic_title','attachment'],
        main_active_flag="brochures",
        active_flag="add_brochures",
        reference_field_name="title",
        template_name="brochures/add_brochures.html",
        title="Add Brochures",
        success_url="allBrochures"
    ), login_url="login"), name="addBrochures"),
    path('deleteBrochures', staff_member_required(ModelListView.as_view(
        model=Brochures,
        template_name="brochures/delete_brochures.html",
        main_active_flag="brochures",
        active_flag="delete_brochures",
        model_name="Brochures",
        title="Delete Brochures"
    ), login_url="login"), name="deleteBrochures"),
    path('deleteBrochure/<slug:slug>', staff_member_required(ModelDeleteView.as_view(
        model=Brochures,
        main_active_flag="brochures",
        active_flag="delete_brochures",
        model_name='Brochures',
        title="Delete Brochures",
        success_url="deleteBrochures"
    ), login_url="login"), name="deleteBrochure"),
    path('editBrochures', staff_member_required(ModelListView.as_view(
        model=Brochures,
        template_name="brochures/edit_brochures.html",
        main_active_flag="brochures",
        active_flag="edit_brochures",
        model_name="Brochures",
        title="Update Brochures"
    ), login_url="login"), name="editBrochures"),
    path('editBrochure/<slug:slug>', staff_member_required(UpdateModelView.as_view(
        model=Brochures,
        fields=['title', 'arabic_title', 'attachment'],
        main_active_flag="brochures",
        active_flag="edit_brochures",
        reference_field_name="title",
        template_name="brochures/edit_brochure.html",
        title="Update Brochures",
        success_url="editBrochures"
    ), login_url="login"), name="editBrochure"),

]