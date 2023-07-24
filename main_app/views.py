import os
import requests
from django.shortcuts import render, redirect, get_object_or_404
import json
from django.http import JsonResponse
from django.db.models import Q
from .forms import CustomSignupForm
from django.contrib.auth import login
from .models import Event, MemberProfile
from .forms import EventForm, MemberProfileForm, ContactForm, MemberSearchForm
from django.utils import timezone
from django.core.mail import send_mail

previous_url = '/'


def index(request):
    global previous_url
    
    previous_url = '/'

    context = {
        
    }

    return render(request, 'index.html', context)


def membership(request):
    global previous_url
    
    user = request.user

    previous_url = '/membership/'

    logged_in = user.is_authenticated

    context = {
        'logged_in': logged_in,
    }

    return render(request, 'membership.html', context)



def signup_view(request):
    global previous_url

    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save(request)
            login(request, user)
            
            if previous_url:
                return redirect(previous_url)
            else:
                return redirect('home')
    else:
        form = CustomSignupForm()
    
    return render(request, 'account/signup.html', {
        'form': form,
    })


def announcements(request):
    global previous_url
    
    user = request.user

    previous_url = '/announcements/'

    logged_in = user.is_authenticated

    is_admin = user.is_superuser

    events = Event.objects.all()

    current_date = timezone.now()

    upcoming_events = Event.objects.filter(end_date__gt=current_date).order_by('start_date')

    past_events = Event.objects.filter(end_date__lt=current_date).order_by('-end_date')

    context = {
        'logged_in': logged_in,
        'is_admin': is_admin,
        'events': events,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    }

    return render(request, 'announcements.html', context)


def edit_event(request, event_short_uuid):
    event = get_object_or_404(Event, event_short_uuid=event_short_uuid)

    if request.method == 'POST':
        if 'delete' in request.POST:
            event.delete()
            return redirect('announcements')
        
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('announcements')
    else:
        form = EventForm(instance=event)
    
    context = {
        'form': form,
        'event': event,
    }
    return render(request, 'create_event.html', context)

def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('announcements')
    else:
        form = EventForm()
    
    context = {
        'form': form
    }
    return render(request, 'create_event.html', context)


def event_detail(request, event_short_uuid):
    event = Event.objects.get(event_short_uuid=event_short_uuid)
    
    context = {
        'event': event
    }

    return render(request, 'event_detail.html', context)


def get_event_data(request):
    events = Event.objects.all()

    events_values = events.values()

    data = {
        'events': list(events_values),
    }

    return JsonResponse(data, safe=False)


def members(request):
    global previous_url
    previous_url = '/members/'

    form = MemberSearchForm()
    members = None
    search_results = False

    if request.method == 'GET':
        form = MemberSearchForm(request.GET)
        if form.is_valid():
            last_name = form.cleaned_data.get('last_name')
            company_organization = form.cleaned_data.get('company_organization')
            state = form.cleaned_data.get('state')
            category = form.cleaned_data.get('category')
            certificate = form.cleaned_data.get('certificate')

            # Query the MemberProfile model based on the search criteria
            members = MemberProfile.objects.all()

            # Apply filters based on search criteria if provided
            if last_name:
                members = members.filter(last_name__icontains=last_name)
            if company_organization:
                members = members.filter(company_organization__icontains=company_organization)

            # Check if state is 'all'; if not, filter by state
            if state and state != 'all':
                members = members.filter(state=state)

            # Check if category is 'all'; if not, filter by category
            if category and category != 'all':
                members = members.filter(category=category)

            # Check if certificate is 'any'; if not, filter by certificate
            if certificate and certificate != 'any':
                members = members.filter(certificate=certificate)

            search_results = True

    context = {
        'members': members,
        'form': form,
        'search_results': search_results,
    }

    # Render the members.html template with the context
    return render(request, 'members.html', context)


def member_profile(request, member_short_uuid):
    user = request.user

    global previous_url

    member_profile, created = MemberProfile.objects.get_or_create(user=user)

    previous_url = f'/profile/{member_short_uuid}'

    context = {
        'user': user,
        'member_profile': member_profile,
        'previous_url': previous_url,
    }

    return render(request, 'member-profile.html', context)


def edit_member_profile(request, member_short_uuid):
    user = request.user
    
    member_profile = get_object_or_404(MemberProfile, user__member_short_uuid=member_short_uuid)

    if request.method == 'POST':
        if 'cancel' in request.POST:
            return redirect('member_profile', member_short_uuid=member_short_uuid)
        form = MemberProfileForm(request.POST, instance=member_profile)
        if form.is_valid():
            form.save()
            return redirect('member_profile', member_short_uuid=member_short_uuid)
    else:
        form = MemberProfileForm(instance=member_profile)
    
    context = {
        'user': user,
        'form': form,
        'member_profile': member_profile,
        'edit_profile': True,
    }
    return render(request, 'member-profile.html', context)


def learn_page(request):
    user = request.user

    global previous_url

    previous_url = f'/learn/'

    context = {
        'user': user,
        'previous_url': previous_url,
    }

    return render(request, 'learn.html', context)


def contact_page(request):
    user = request.user

    global previous_url

    previous_url = f'/contact/'

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            send_contact_email(form.cleaned_data)  # Send the email
            return redirect('announcements')
    else:
        form = ContactForm()

    context = {
        'user': user,
        'previous_url': previous_url,
        'form': form,
    }

    return render(request, 'contact.html', context)


def send_contact_email(data):
    subject = 'New Contact Message'
    message = f"Name: {data['name']}\nEmail: {data['email']}\n\n{data['message']}"
    from_email = os.environ.get('CONTACT_FROM_EMAIL')  # Update with your email address
    to_email = [os.environ.get('CONTACT_TO_EMAIL')]  # Update with the recipient's email address
    send_mail(subject, message, from_email, to_email)
