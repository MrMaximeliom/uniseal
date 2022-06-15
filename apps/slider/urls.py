from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from apps.common_code.views import ModelDeleteView, AddModelView, UpdateModelView, ModelListView
from apps.slider.models import Slider

urlpatterns = [
    path('allSliders', staff_member_required(ModelListView.as_view(
        model=Slider,
        template_name="slider/all_sliders.html",
        main_active_flag="sliders",
        active_flag="all_sliders",
        model_name="Slider",
        title="All Sliders"
    ), login_url="login"), name="allSliders"),
    path('addSliders', staff_member_required(AddModelView.as_view(
        model=Slider,
        fields=['title', 'arabic_title',
                'image', 'link'],
        main_active_flag="sliders",
        active_flag="add_sliders",
        reference_field_name="title",
        template_name="slider/add_sliders.html",
        title="Add Sliders",
        success_url="allSliders"
    ), login_url="login"), name="addSliders"),
    path('editSliders', staff_member_required(ModelListView.as_view(
        model=Slider,
        template_name="slider/edit_sliders.html",
        main_active_flag="sliders",
        active_flag="edit_sliders",
        model_name="Slider",
        title="Edit Sliders"
    ), login_url="login"), name="editSliders"),
    path('editSlider/<str:slug>', staff_member_required(UpdateModelView.as_view(
        model=Slider,
        fields=['title', 'arabic_title',
                'image', 'link'],
        main_active_flag="sliders",
        active_flag="edit_sliders",
        reference_field_name="title",
        template_name="slider/edit_slider.html",
        title="Edit Sliders",
        success_url="allSliders"
    ), login_url="login"), name="editSlider"),
    path('deleteSliders', staff_member_required(ModelListView.as_view(
        model=Slider,
        template_name="slider/delete_sliders.html",
        main_active_flag="sliders",
        active_flag="delete_sliders",
        model_name="Slider",
        title="Delete Sliders"
    ), login_url="login"), name="deleteSliders"),
    path('deleteSlider/<slug:slug>', staff_member_required(ModelDeleteView.as_view(
        model=Slider,
        main_active_flag="sliders",
        active_flag="delete_sliders",
        model_name='Slider',
        title="Delete Sliders",
        success_url="deleteSliders"
    ), login_url="login"), name="deleteSlider"),
    ]