from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from apps.common_code.views import ModelDeleteView, AddModelView, UpdateModelView
from apps.sellingPoint import dashboard_views as selling_point_views
from apps.sellingPoint.dashboard_views import SellingPointsListView
from apps.sellingPoint.models import SellingPoint

urlpatterns = [
    path('allSellingPoints', staff_member_required(SellingPointsListView.as_view(
        model=SellingPoint,
        template_name="sellingPoints/all_selling_points.html",
        main_active_flag="selling_points",
        active_flag="all_selling_points",
        model_name="Selling Point",
        title="All Selling Points"
    ), login_url="login"), name="allSellingPoints"),
    path('addSellingPoints', staff_member_required(AddModelView.as_view(
        model=SellingPoint,
        fields=['name', 'arabic_name',
                'image', 'location', 'address',
                'country', 'state',
                'city', 'area', 'phone_number', 'secondary_phone','email'],
        main_active_flag="selling_points",
        active_flag="add_selling_points",
        reference_field_name="name",
        template_name="sellingPoints/add_selling_points.html",
        title="Add Selling Points",
        success_url="allSellingPoints"
    ), login_url="login"), name="addSellingPoints"),
    path('deleteSellingPoints', staff_member_required(SellingPointsListView.as_view(
        model=SellingPoint,
        template_name="sellingPoints/delete_selling_points.html",
        main_active_flag="selling_points",
        active_flag="delete_selling_points",
        model_name="Selling Point",
        title="Delete Selling Points"
    ), login_url="login"), name="deleteSellingPoints"),
    path('deleteSellingPoint/<slug:slug>', staff_member_required(ModelDeleteView.as_view(
        model=SellingPoint,
        main_active_flag="selling_points",
        active_flag="delete_selling_points",
        model_name='Selling Point',
        title="Delete Selling Points",
        success_url="deleteSellingPoints"
    ), login_url="login"), name="deleteSellingPoint"),
    path('editSellingPoints', staff_member_required(SellingPointsListView.as_view(
        model=SellingPoint,
        template_name="sellingPoints/edit_selling_points.html",
        main_active_flag="selling_points",
        active_flag="edit_selling_points",
        model_name="Selling Point",
        title="Edit Selling Points"
    ), login_url="login"), name="editSellingPoints"),
    path('editSellingPoint/<str:slug>', staff_member_required(UpdateModelView.as_view(
        model=SellingPoint,
        fields=['name', 'arabic_name',
                'image', 'location', 'address',
                'country', 'state',
                'city', 'area', 'phone_number', 'secondary_phone', 'email'],
        main_active_flag="selling_points",
        active_flag="add_selling_points",
        reference_field_name="name",
        template_name="sellingPoints/edit_selling_point.html",
        title="Edit Selling Points",
        success_url="allSellingPoints"
    ), login_url="login"), name="editSellingPoint"),
    path('sellingPointDetails/<str:slug>', selling_point_views.selling_point_details, name='sellingPointDetails'),

]