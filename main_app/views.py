import os
import requests
from django.shortcuts import render, redirect, get_object_or_404
import json
from django.http import JsonResponse
from django.db.models import Q
from .forms import CustomSignupForm
from django.contrib.auth import login
from .models import Event
from .forms import EventForm
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


def edit_event(request, unique_event_id):
    event = get_object_or_404(Event, unique_event_id=unique_event_id)

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


def event_detail(request, unique_event_id):
    event = Event.objects.get(unique_event_id=unique_event_id)
    
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
