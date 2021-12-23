from django.urls import path

from slider import dashboard_views as slider_views

urlpatterns = [
    path('allSliders', slider_views.all_sliders, name='allSliders'),
    path('addSliders', slider_views.add_sliders, name='addSliders'),
    path('deleteSliders', slider_views.delete_sliders, name='deleteSliders'),
    path('editSliders', slider_views.edit_sliders, name='editSliders'),
    path('editSlider/<str:slug>', slider_views.edit_slider, name='editSlider'),
    path('deleteSlider/<int:id>', slider_views.confirm_delete, name='deleteSlider'),

    ]