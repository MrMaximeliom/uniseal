from django.urls import path

from apps.orders import dashboard_views as orders_views

urlpatterns = [
    path('allOrders', orders_views.all_orders, name='allOrders'),
    path('orderDetails/<str:slug>', orders_views.edit_order, name='editOrder'),
]