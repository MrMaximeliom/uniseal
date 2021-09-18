from django.urls import path

from sellingPoint import dashboard_views as selling_point_views

urlpatterns = [
    path('allSellingPoints', selling_point_views.all_selling_points, name='allSellingPoints'),
    path('addSellingPoints', selling_point_views.add_selling_points, name='addSellingPoints'),
    path('deleteSellingPoints', selling_point_views.delete_selling_points, name='deleteSellingPoints'),
    path('editSellingPoints', selling_point_views.edit_selling_points, name='editSellingPoints'),
    path('editSellingPoint/<str:slug>', selling_point_views.edit_selling_point, name='editSellingPoint'),
    path('sellingPointDetails/<str:slug>', selling_point_views.selling_point_details, name='sellingPointDetails'),
    path('deleteSellingPoint/<int:id>', selling_point_views.confirm_delete, name='deleteSellingPoint'),

]