from django.shortcuts import render, redirect, get_object_or_404
from .models import Event
from django.utils import timezone
from membership.models import Membership
from resources.models import Resource, Folder


def events(request):
    events = Event.objects.all()

    current_datetime = timezone.now()

    upcoming_events = Event.objects.filter(date__gt=current_datetime).order_by('date')

    past_events = Event.objects.filter(date__lt=current_datetime).order_by('-date')

    context = {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    }

    return render(request, 'events/events.html', context)


def event_detail(request, event_name):
    event = get_object_or_404(Event, name=event_name)

    user = request.user
    
    membership = Membership.objects.get(user=user)

    if membership.status.valid:
        display_folder = True
        folders = Folder.objects.filter(parent_folder=event.folder)
        resources = Resource.objects.filter(folder=event.folder)
    else:
        display_folder = False
        folders = False
        resources = False

    context = {
        'event': event,
        'display_folder': display_folder,
        'folders': folders,
        'resources': resources,
    }

    return render(request, 'events/event_detail.html', context)