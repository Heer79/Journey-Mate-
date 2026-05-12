from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Booking
from django.core.mail import send_mail
from django.conf import settings

@receiver(pre_save, sender=Booking)
def send_approval_email(sender, instance, **kwargs):
    """Send an email when a booking transitions to APPROVED status."""
    if instance.pk:
        try:
            old_booking = Booking.objects.get(pk=instance.pk)
        except Booking.DoesNotExist:
            return
        if old_booking.approval_status != 'APPROVED' and instance.approval_status == 'APPROVED':
            send_mail(
                subject=f"Booking Approved - {instance.package.name}",
                message=(
                    f"Hello {instance.user.username},\n\n"
                    f"Your booking for {instance.package.name} has been approved.\n"
                    f"You can download your invoice from your dashboard."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.user.email],
                fail_silently=True,
            )
    else:
        # New booking auto-approved
        if instance.approval_status == 'APPROVED':
            send_mail(
                subject=f"Booking Confirmed - {instance.package.name}",
                message=(
                    f"Hello {instance.user.username},\n\n"
                    f"Your booking for {instance.package.name} has been confirmed.\n"
                    f"You can download your invoice from your dashboard after payment."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.user.email],
                fail_silently=True,
            )

