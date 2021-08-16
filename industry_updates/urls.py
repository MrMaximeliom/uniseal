from django.urls import path
from industry_updates import views as updates_views
urlpatterns = [
    path('allUpdates', updates_views.all_updates, name='allUpdates'),
    path('addUpdates', updates_views.add_updates, name='addUpdates'),
    path('deleteUpdates', updates_views.delete_updates, name='deleteUpdates'),
    path('editUpdates', updates_views.edit_updates, name='editUpdates'),
    path('editUpdate/<str:slug>', updates_views.edit_update, name='editUpdate'),
    path('deleteUpdate/<int:id>', updates_views.confirm_delete, name='deleteUpdate'),

    ]