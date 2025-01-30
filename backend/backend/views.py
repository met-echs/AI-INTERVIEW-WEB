from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail
from .forms import ContactForm

def home(request):
    return render(request, 'Home/index.html')

def contact_form(request):
    if request.method == "POST":
        fullname = request.POST.get('fullname')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        msg = request.POST.get('msg')
        admin_mail="amilmether37@gmail.com"
        # Send Email (if configured)
        send_mail(
            subject=f"New Contact Form Submission from {fullname}",
            message=f"Name: {fullname}\nPhone: {phone}\nEmail: {email}\nMessage: {msg}",
            from_email=email,
            recipient_list=[admin_mail],
            fail_silently=False
        )

        return JsonResponse({'success': True})

    return render(request, 'Home/Contact.html')


