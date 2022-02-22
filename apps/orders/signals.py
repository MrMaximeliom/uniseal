from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.orders.models import Order,Cart

@receiver(post_save, sender=Cart)
def calculate_total_contact(sender, instance, created, **kwargs):
    if created:
        order  = Order.objects.get(id=instance.order.id)
        order.total += instance.product.price * instance.quantity
        order.save()







