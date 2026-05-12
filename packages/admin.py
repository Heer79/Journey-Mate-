from django.contrib import admin
from .models import Category, Package, Offer

class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'bus_type', 'total_seats_available', 'created_at')
    list_filter = ('category', 'bus_type')
    search_fields = ('name', 'description')

admin.site.register(Category)
admin.site.register(Package, PackageAdmin)
admin.site.register(Offer)
