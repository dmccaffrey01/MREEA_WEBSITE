from django.shortcuts import render, redirect
import os
from django.contrib import messages
from .forms import ContactForm
from django.core.mail import EmailMessage, BadHeaderError


def contact(request):
    """A view to render the contact page"""

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            if send_contact_email(form.cleaned_data, request):  # Pass request to send_contact_email
                messages.success(request, 'Your message has been sent. Thank you!')
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
    }

    return render(request, 'contact/contact.html', context)


def send_contact_email(data, request):
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
    
    try:
        email.send()
        return True
    except BadHeaderError:
        messages.error(request, 'Invalid header found.')
        return False
    except Exception as e:
        messages.error(request, 'There was an error sending your message. Please try again later.')
        return False
