from django.shortcuts import render, redirect, get_object_or_404
from .models import Event
from django.utils import timezone


def events(request):
    events = Event.objects.all()

    current_datetime = timezone.now()

    upcoming_events = Event.objects.filter(date__gt=current_datetime).order_by('date')[:3]

    past_events = Event.objects.filter(date__lt=current_datetime).order_by('-date')[:3]

    context = {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    }

    return render(request, 'events/events.html', context)