from django.db import models
from django.conf import settings
from packages.models import Package, Offer

class Booking(models.Model):
    PAYMENT_CHOICES = [
        ('ONLINE', 'Online Payment'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
    ]
    APPROVAL_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    travel_date = models.DateField()
    no_of_passengers = models.PositiveIntegerField(default=1)
    offer_applied = models.ForeignKey(Offer, on_delete=models.SET_NULL, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='ONLINE')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    approval_status = models.CharField(max_length=20, choices=APPROVAL_STATUS_CHOICES, default='PENDING')

    # Razorpay Fields
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Booking {self.id} - {self.user.username} - {self.package.name}"
