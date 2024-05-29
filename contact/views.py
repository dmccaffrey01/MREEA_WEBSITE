from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
import os
from django.contrib import messages

from .forms import ContactForm


def contact(request):
    """A view to render the contact page"""

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            send_contact_email(form.cleaned_data)
            messages.success(request, 'Your message has been sent, Thank you')
            return redirect('home')
    else:
        form = ContactForm()

    context = {
        'form': form,
    }

    return render(request, 'contact/contact.html', context)


def send_contact_email(data):
    """
    Send a contact email
    """
    subject = 'New Contact Message From Website'
    message = f"Name: {data['name']}\n"\
              f"Email: {data['email']}\n\n"\
              f"Message: {data['message']}"
    from_email = os.environ.get('CONTACT_FROM_EMAIL')
    to_email = [os.environ.get('CONTACT_TO_EMAIL')]
    reply_to = [data['email']]
    
    email = EmailMessage(
        subject,
        message,
        from_email,
        to_email,
        reply_to=reply_to,
    )

    email.send()
