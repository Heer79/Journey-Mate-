from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:package_id>/', views.booking_create, name='booking_create'),
    path('check-availability/<int:package_id>/', views.check_availability, name='check_availability'),
    path('payment/<int:booking_id>/', views.payment_initiate, name='payment_initiate'),
    path('payment-callback/', views.payment_callback, name='payment_callback'),
    path('invoice/<int:booking_id>/', views.invoice_download, name='invoice_download'),
]
