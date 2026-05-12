from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from packages.models import Package, Offer
from .models import Booking
from django.utils import timezone
from decimal import Decimal
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import razorpay
from datetime import datetime as dt, date as date_cls, timedelta
from django.db.models import Sum

try:
    razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
except Exception:
    razorpay_client = None

@login_required
def payment_initiate(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.payment_status == 'PAID':
        messages.info(request, "This booking is already paid.")
        return redirect('dashboard')
        
    amount_in_paise = int(booking.total_amount * 100)
    
    if not booking.razorpay_order_id:
        try:
            if razorpay_client and settings.RAZORPAY_KEY_ID != 'rzp_test_YourDummyKeyHere':
                razorpay_order = razorpay_client.order.create(dict(
                    amount=amount_in_paise,
                    currency='INR',
                    payment_capture='1'
                ))
                booking.razorpay_order_id = razorpay_order['id']
            else:
                booking.razorpay_order_id = f"mock_order_{booking.id}"
        except Exception:
            booking.razorpay_order_id = f"mock_order_{booking.id}"
        booking.save()
        
    context = {
        'booking': booking,
        'razorpay_key': settings.RAZORPAY_KEY_ID,
        'amount': amount_in_paise,
        'razorpay_order_id': booking.razorpay_order_id,
        'callback_url': request.build_absolute_uri('/bookings/payment-callback/')
    }
    return render(request, 'bookings/payment.html', context)

@csrf_exempt
def payment_callback(request):
    if request.method == "POST":
        payment_id = request.POST.get('razorpay_payment_id', '')
        order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')
        
        try:
            booking = Booking.objects.get(razorpay_order_id=order_id)
            
            # Handle mock flow bypass
            if order_id.startswith('mock_order_') or signature == 'mock_signature_success':
                booking.razorpay_payment_id = payment_id
                booking.razorpay_signature = signature
                booking.payment_status = 'PAID'
                booking.save()
                messages.success(request, "[DEMO] Mock Payment successfully processed! Your invoice is ready.")
                return redirect('dashboard')
            
            if razorpay_client:
                params_dict = {
                    'razorpay_order_id': order_id,
                    'razorpay_payment_id': payment_id,
                    'razorpay_signature': signature
                }
                razorpay_client.utility.verify_payment_signature(params_dict)
            
            booking.razorpay_payment_id = payment_id
            booking.razorpay_signature = signature
            booking.payment_status = 'PAID'
            booking.save()
            
            messages.success(request, "Payment successfully processed via Razorpay! Your invoice is ready.")
            return redirect('dashboard')
            
        except Exception as e:
            messages.error(request, "Payment verification failed. Please try again.")
            return redirect('dashboard')
    
    return redirect('dashboard')

def check_availability(request, package_id):
    """AJAX endpoint: returns seats available for a package on a specific date."""
    package = get_object_or_404(Package, id=package_id)
    travel_date = request.GET.get('date', '')
    try:
        td = dt.strptime(travel_date, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return JsonResponse({'available_seats': package.total_seats_available})

    # Count passengers already booked on this date (exclude rejected/pending-payment cancelled)
    booked = Booking.objects.filter(
        package=package,
        travel_date=td,
        approval_status='APPROVED'
    ).exclude(payment_status='PENDING').aggregate(
        total=Sum('no_of_passengers')
    )['total'] or 0

    available = max(package.total_seats_available - booked, 0)
    return JsonResponse({'available_seats': available})


@login_required
def booking_create(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    
    if request.method == 'POST':
        travel_date = request.POST.get('travel_date')
        no_of_passengers = int(request.POST.get('no_of_passengers', 1))
        payment_method = request.POST.get('payment_method')
        offer_code = request.POST.get('offer_code', '').strip()

        # Server-side date validation
        try:
            td = dt.strptime(travel_date, '%Y-%m-%d').date()
            today = date_cls.today()
            max_date = today + timedelta(days=730)
            if td < today:
                messages.error(request, "Travel date cannot be in the past. Please choose a valid date.")
                return redirect('booking_create', package_id=package.id)
            if td > max_date:
                messages.error(request, "Travel date cannot be more than 2 years in the future.")
                return redirect('booking_create', package_id=package.id)
        except (ValueError, TypeError):
            messages.error(request, "Invalid travel date. Please select a date using the date picker.")
            return redirect('booking_create', package_id=package.id)
        
        # Per-date seat availability check
        booked_on_date = Booking.objects.filter(
            package=package,
            travel_date=td,
            approval_status='APPROVED'
        ).exclude(payment_status='PENDING').aggregate(
            total=Sum('no_of_passengers')
        )['total'] or 0
        available_seats = max(package.total_seats_available - booked_on_date, 0)

        if available_seats < no_of_passengers:
            messages.error(request, f"Sorry, only {available_seats} seats are available for {travel_date}.")
            return redirect('booking_create', package_id=package.id)
            
        total_price = package.price * no_of_passengers
        offer_applied = None
        
        if offer_code:
            try:
                offer = Offer.objects.get(code__iexact=offer_code, active=True, valid_until__gte=timezone.now())
                discount_amount = total_price * Decimal(offer.discount_percent) / Decimal(100)
                total_price -= discount_amount
                offer_applied = offer
                messages.success(request, f"Offer code '{offer_code}' applied! You saved ₹{discount_amount:.2f}.")
            except Offer.DoesNotExist:
                messages.warning(request, "Invalid or expired offer code. Proceeding without discount.")
                
        # Create booking (Auto-Approved & Pending Payment)
        booking = Booking.objects.create(
            user=request.user,
            package=package,
            travel_date=travel_date,
            no_of_passengers=no_of_passengers,
            offer_applied=offer_applied,
            total_amount=total_price,
            payment_method='ONLINE',
            payment_status='PENDING',
            approval_status='APPROVED'
        )
        
        messages.success(request, "Booking details secured! Redirecting to payment checkout...")
        return redirect('payment_initiate', booking_id=booking.id)

    return render(request, 'bookings/create.html', {'package': package})

@login_required
def invoice_download(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.approval_status != 'APPROVED' or booking.payment_status != 'PAID':
        messages.warning(request, "Invoice is only available for approved and fully paid bookings.")
        return redirect('dashboard')
        
    template_path = 'bookings/invoice.html'
    context = {'booking': booking}
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="JourneyMate_Invoice_{booking.id}.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)
    
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
