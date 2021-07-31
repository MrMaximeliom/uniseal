from django.urls import path
from brochures import views as brochures_views

urlpatterns = [
    path('allBrochures', brochures_views.all_brochures, name='allBrochures'),
    path('addBrochures', brochures_views.add_brochures, name='addBrochures'),
    path('deleteBrochures', brochures_views.delete_brochures, name='deleteBrochures'),
    path('editBrochures', brochures_views.edit_brochures, name='editBrochures'),
    path('deleteBrochure/<int:id>', brochures_views.confirm_delete, name='deleteBrochure'),
    path('editBrochure/<str:slug>', brochures_views.edit_brochure, name='editBrochure'),

]