from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from apps.orders.models import Order


# from django.contrib.auth import user_logged_in, user_logged_out
# from django.dispatch.dispatcher import receiver as receiver_second
# from django.contrib.sessions.models import Session


# عند تسجيل مستخدم جديد يتم إنشاء ملف شخصي خاص به تلقائيا
@receiver(post_save, sender=Order)
def create_sms_contact(sender, instance, created, **kwargs):
    from apps.orders.models import Cart
    carts = Cart.objects.filter(order=instance)
    total = 0.0
    if created:
        for cart in carts:
            total_cart_price = cart.product.price * cart.quantity
            total = total_cart_price+ total
        instance.total = total





