from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Package(models.Model):
    BUS_CHOICES = [
        ('AC', 'AC Bus'),
        ('NON_AC', 'Non-AC Bus'),
    ]
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bus_type = models.CharField(max_length=20, choices=BUS_CHOICES, default='AC')
    hotel_details = models.TextField()
    day_night_duration = models.CharField(max_length=100, help_text="e.g., 3 Days / 2 Nights")
    total_seats_available = models.PositiveIntegerField(default=40)
    image = models.ImageField(upload_to='packages/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Offer(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percent = models.PositiveIntegerField(help_text="Discount percentage (0-100)")
    valid_until = models.DateTimeField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
