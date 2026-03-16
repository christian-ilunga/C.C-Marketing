from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings


def home(request: HttpRequest) -> HttpResponse:
    """
    Landing page for the social media marketer.

    Handles simple contact form submission and sends an email to the configured address.
    """
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        message = request.POST.get("message", "").strip()

        if not (name and email and message):
            messages.error(request, "Please fill in all fields before sending your message.")
        else:
            subject = f"New enquiry from {name}"
            body = f"From: {name} <{email}>\n\nMessage:\n{message}"
            recipient = getattr(settings, "CONTACT_EMAIL", None) or getattr(
                settings, "DEFAULT_FROM_EMAIL", None
            )

            if recipient:
                try:
                    send_mail(
                        subject=subject,
                        message=body,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[recipient],
                    )
                    messages.success(
                        request,
                        "Thank you for reaching out! I have received your message and will get back to you shortly.",
                    )
                except BadHeaderError:
                    messages.error(request, "There was a problem sending your message. Please try again.")
            else:
                # If email is not configured yet, show a friendly message.
                messages.warning(
                    request,
                    "The contact form is not fully configured yet. Please check back soon or reach out via WhatsApp.",
                )

    context = {
        "page_title": "Social Media Marketing",
    }
    return render(request, "marketing/home.html", context)

# Create your views here.
