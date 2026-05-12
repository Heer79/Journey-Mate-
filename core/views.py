from django.shortcuts import render, redirect
from packages.models import Package
from .forms import ContactMessageForm
from django.contrib import messages

def home(request):
    # Get featured packages (for now just latest 3)
    featured_packages = Package.objects.order_by('-created_at')[:3]
    return render(request, 'core/home.html', {'featured_packages': featured_packages})

def contact_view(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent! We will get back to you shortly.")
            return redirect('contact')
    else:
        form = ContactMessageForm()
    return render(request, 'core/contact.html', {'form': form})

def feedback_view(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            # Optionally prefix the subject with [Feedback]
            feedback_msg = form.save(commit=False)
            feedback_msg.subject = f"[Feedback] {feedback_msg.subject}"
            feedback_msg.save()
            messages.success(request, "Thank you for your feedback! It helps us improve.")
            return redirect('feedback')
    else:
        form = ContactMessageForm()
    return render(request, 'core/feedback.html', {'form': form})
