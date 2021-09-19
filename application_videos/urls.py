from django.urls import path

from application_videos import dashboard_views as product_videos_views

urlpatterns = [
    path('allVideos', product_videos_views.all_videos, name='allVideos'),
    path('productVideos/<str:slug>', product_videos_views.product_videos, name='productVideos'),
    path('productVideos/', product_videos_views.product_videos, name='productVideos-dash'),
    path('deleteVideos', product_videos_views.delete_products_videos, name='deleteVideos'),
    path('confirmDelete/<int:id>', product_videos_views.confirm_delete, name='videoDelete'),
    path('editVideo/<str:slug>', product_videos_views.edit_video, name='editVideo'),
    path('editVideos', product_videos_views.edit_videos, name='editVideos'),




]
#     path('addProducts', product_views.add_products, name='addProducts'),
#     path('deleteProducts', product_views.delete_products, name='deleteProducts'),
#     path('editProduct/<str:slug>', product_views.edit_product, name='editProduct'),
#     path('editProducts', product_views.edit_products, name='editProducts'),
#     path('productDetails/<str:slug>', product_views.product_details, name='productDetails'),
#     path('confirmDelete/<int:id>', product_views.confirm_delete, name='productDelete'),]