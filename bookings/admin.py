from django.contrib import admin
from .models import Booking

class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'package', 'travel_date', 'no_of_passengers', 'payment_status', 'approval_status')
    list_filter = ('payment_status', 'approval_status', 'travel_date')
    search_fields = ('user__username', 'package__name')

admin.site.register(Booking, BookingAdmin)
