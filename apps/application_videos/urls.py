from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from apps.application_videos import dashboard_views as product_videos_views
from apps.application_videos.dashboard_views import VideosListView
from apps.application_videos.models import ProductApplicationVideos
from apps.common_code.views import ModelDeleteView, UpdateModelView

urlpatterns = [
    path('allVideos', staff_member_required(VideosListView.as_view(
        model=ProductApplicationVideos,
        template_name="application_videos/all_videos.html",
        main_active_flag="videos",
        active_flag="all_videos",
        model_name="ProductVideos",
        title="All Products' Videos"
    ), login_url="login"), name="allVideos"),
    path('productVideos/', product_videos_views.product_videos, name='productVideos-dash'),
    path('productVideos/<str:slug>', product_videos_views.product_videos, name='productVideos'),
    path('deleteVideos', staff_member_required(VideosListView.as_view(
        model=ProductApplicationVideos,
        template_name="application_videos/delete_videos.html",
        main_active_flag="videos",
        active_flag="delete_videos",
        model_name="ProductVideos",
        title="Delete Products' Videos"
    ), login_url="login"), name="deleteVideos"),
    path('deleteVideo/<slug:slug>', staff_member_required(ModelDeleteView.as_view(
        model=ProductApplicationVideos,
        main_active_flag="videos",
        active_flag="delete_videos",
        model_name="ProductVideos",
        title="Delete Products' Videos",
        success_url="deleteVideos"
    ), login_url="login"), name="videoDelete"),
    path('editVideos', staff_member_required(VideosListView.as_view(
        model=ProductApplicationVideos,
        template_name="application_videos/edit_videos.html",
        main_active_flag="videos",
        active_flag="edit_videos",
        model_name="ProductVideos",
        title="Edit Products' Videos",
    ), login_url="login"), name="editVideos"),
    path('editVideo/<slug:slug>', staff_member_required(UpdateModelView.as_view(
        model=ProductApplicationVideos,
        fields=['application_video','product'],
        active_flag="edit_videos",
        main_active_flag="videos",
        reference_field_name="name",
        template_name="application_videos/edit_video.html",
        title="Update Country",
        success_url="editCountries"
    ), login_url="login"), name="editVideo"),

]
