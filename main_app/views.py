import os
import requests
from django.shortcuts import render, redirect, get_object_or_404
import json
from django.http import JsonResponse
from django.db.models import Q
from .forms import CustomSignupForm
from django.contrib.auth import login
from .models import Event, MemberProfile
from .forms import EventForm, MemberProfileForm
from django.utils import timezone


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
    if previous_url.endswith('/membership/'):
        membership = True
    else:
        membership = False

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
        'membership': membership,
    })


def announcements(request):
    global previous_url
    
    user = request.user

    previous_url = '/announcements/'

    logged_in = user.is_authenticated

    is_admin = user.is_superuser

    events = Event.objects.all()

    current_date = timezone.now()

    upcoming_events = Event.objects.filter(start_date__gt=current_date).order_by('start_date')

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

    context = {
        
    }

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
    member_profile = get_object_or_404(MemberProfile, user__member_short_uuid=member_short_uuid)

    if request.method == 'POST':
        form = MemberProfileForm(request.POST, instance=member_profile)
        if form.is_valid():
            form.save()
            return redirect('member_profile', member_short_uuid=member_short_uuid)
    else:
        form = MemberProfileForm(instance=member_profile)
    
    context = {
        'form': form,
        'member_profile': member_profile,
    }
    return render(request, 'edit_profile.html', context)
