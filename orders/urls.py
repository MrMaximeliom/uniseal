from django.urls import path

from orders import dashboard_views as orders_views

urlpatterns = [
    path('allOrders', orders_views.all_orders, name='allOrders'),

    ]