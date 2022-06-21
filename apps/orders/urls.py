from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required
from apps.orders.dashboard_views import OrderListView
from apps.orders.models import Order

from apps.orders import dashboard_views as orders_views

urlpatterns = [
    # path('allOrders', orders_views.all_orders, name='allOrders'),
    path('allOrders', staff_member_required(OrderListView.as_view(
        model=Order,
        template_name="orders/all_orders.html",
        main_active_flag="orders",
        active_flag="all_orders",
        model_name="Order",
        title="All Orders"
    ), login_url="login"), name="allOrders"),
    path('orderDetails/<str:slug>', orders_views.edit_order, name='editOrder'),
]