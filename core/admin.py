from django.contrib import admin
from .models import ContactMessage

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'email', 'created_at', 'resolved')
    list_filter = ('resolved', 'created_at')

admin.site.register(ContactMessage, ContactMessageAdmin)
