from django.urls import path
from working_field import views as working_views
urlpatterns = [
    path('allFields', working_views.all_fields, name='allFields'),
    path('addFields', working_views.add_fields, name='addFields'),
    path('deleteFields', working_views.delete_fields, name='deleteFields'),
    path('deleteField/<int:id>', working_views.confirm_delete, name='deleteField'),
    path('editFields', working_views.edit_fields, name='editFields'),
    path('editField/<str:slug>', working_views.edit_field, name='editField'),
    ]