# orders/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OrderItem
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=OrderItem)
def notify_vendor_on_new_order(sender, instance, created, **kwargs):
    """
    Send notification to vendor when their product is ordered
    """
    if created:
        order = instance.order
        product = instance.product
        vendor = product.vendor
        
        # Prepare email notification
        subject = f"New Order Received - Order #{order.id}"
        message = f"""
        Hello {vendor.business_name},
        
        A new order has been placed containing your product:
        
        Order #: {order.id}
        Product: {product.name}
        Quantity: {instance.quantity}
        Amount: ${instance.subtotal}
        
        Please log in to your account to view the full order details.
        
        Thank you,
        E-commerce Team
        """
        
        # In a real app, you would send an actual email
        print(f"Sending email to {vendor.user.email}: {subject}")
        
        # For production, uncomment below to actually send emails
        # send_mail(
        #     subject,
        #     message,
        #     settings.DEFAULT_FROM_EMAIL,
        #     [vendor.user.email],
        #     fail_silently=False,
        # )