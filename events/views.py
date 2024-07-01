from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import Event
from django.utils import timezone
from datetime import timedelta
from resources.models import Resource, Folder, Icon
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import EventForm
from .tasks import new_event_notifications
import os


def events(request):
    all_events = Event.objects.all()

    public_events = all_events.filter(is_public=True)

    current_datetime = timezone.localtime(timezone.now())
    tomorrow_start = current_datetime + timedelta(days=1)
    tomorrow_start = tomorrow_start.replace(hour=0, minute=0, second=0, microsecond=0)

    upcoming_events_query = public_events.filter(date__gte=tomorrow_start).order_by('date')
    past_events_query = public_events.filter(date__lt=tomorrow_start).order_by('-date')

    if request.method == 'POST':
        viewAllValue = request.POST.get('id_view_all')

        if viewAllValue == 'upcoming':
            upcoming_slice = upcoming_events_query.count()
            past_slice = 4
        else:
            past_slice = past_events_query.count()
            upcoming_slice = 4
    else:
        upcoming_slice = 4
        past_slice = 4

    draft_events = all_events.filter(is_public=False)
    upcoming_events = upcoming_events_query[:upcoming_slice]
    past_events = past_events_query[:past_slice]

    context = {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'draft_events': draft_events,
    }

    return render(request, 'events/events.html', context)


@login_required
def add_event(request):

    user = request.user

    if not user.is_superuser:
        messages.error(request, "You must be an admin to add an event!")
        return redirect(reverse('events'))
    
    if request.method == 'POST':
        form = EventForm(request.POST)

        if form.is_valid():
            form_data = form.cleaned_data
            event_friendly_name = form_data['friendly_name']
            event_description = form_data['description']
            event_date = form_data['date']
            event_time = form_data['time']
            event_location = form_data['location']
            event_is_public = form_data['is_public']

            events_parent_folder = Folder.objects.filter(name='events').first()
            folder_icon = Icon.objects.filter(name='folder').first()
            new_folder, created = Folder.objects.get_or_create(
                friendly_name=event_friendly_name,
                parent_folder=events_parent_folder,
                icon=folder_icon
            )
            new_folder.save()

            register_url = request.POST.get("id_register_url", None)
            google_drive_url = request.POST.get("id_google_drive_url", None)

            if register_url:
                register_friendly_name = 'Event Register Link'
                register_icon = Icon.objects.filter(name="register").first()

                new_register_resource = Resource.objects.create(
                    friendly_name=register_friendly_name,
                    folder=new_folder,
                    url=register_url,
                    icon=register_icon
                )
                new_register_resource.save()
            else:
                new_register_resource = False

            if google_drive_url:
                google_drive_friendly_name = 'Google Drive Folder'
                google_drive_icon = Icon.objects.filter(name="google_drive").first()

                new_google_drive_resource = Resource.objects.create(
                    friendly_name=google_drive_friendly_name,
                    folder=new_folder,
                    url=google_drive_url,
                    icon=google_drive_icon
                )
                new_google_drive_resource.save()
            else:
                new_google_drive_resource = False
            
            new_event = Event.objects.create(
                friendly_name=event_friendly_name,
                description=event_description,
                date=event_date,
                time=event_time,
                location=event_location,
                folder=new_folder,
                is_public=event_is_public,
            )

            if new_register_resource:
                new_event.register_link = new_register_resource
            if new_google_drive_resource:
                new_event.google_drive_link = new_google_drive_resource

            new_event.save()

            if event_is_public:
                new_event_notifications(new_event.name)

            messages.success(request, 'Successfully created event!')

            return redirect(reverse('events'))
    else:
        form = EventForm()

    action_url = reverse('add_event')

    context = {
        'form': form,
        'register_url': '',
        'google_drive_url': '',
        'action_url': action_url,
        'page_heading': 'Add',
    }

    return render(request, 'events/event.html', context)


@login_required
def edit_event(request, event_name):

    user = request.user

    if not user.is_superuser:
        messages.error(request, "You must be an admin to edit an event!")
        return redirect(reverse('events'))
    
    selected_event = Event.objects.filter(name=event_name).first()

    if not selected_event:
        messages.error(request, "Invalid event!")
        return redirect(reverse('events'))
    
    if request.method == 'POST':
        form = EventForm(request.POST)

        if form.is_valid():
            form_data = form.cleaned_data
            event_friendly_name = form_data['friendly_name']
            event_description = form_data['description']
            event_date = form_data['date']
            event_time = form_data['time']
            event_location = form_data['location']
            event_is_public = form_data['is_public']

            register_url = request.POST.get("id_register_url", '')
            register_name = request.POST.get("id_register_name", '')
            google_drive_url = request.POST.get("id_google_drive_url", '')
            google_drive_name = request.POST.get("id_google_drive_name", '')

            register_friendly_name = 'Event Register Link'
            register_icon = Icon.objects.filter(name="register").first()

            if register_name:
                new_register_resource = Resource.objects.filter(name=register_name).first()
                new_register_resource.url = register_url
            else:
                new_register_resource = Resource.objects.create(
                    friendly_name=register_friendly_name,
                    folder=selected_event.folder,
                    url=register_url,
                    icon=register_icon
                )
            new_register_resource.save()

            google_drive_friendly_name = 'Google Drive Folder'
            google_drive_icon = Icon.objects.filter(name="google_drive").first()

            if register_name:
                new_google_drive_resource = Resource.objects.filter(name=google_drive_name).first()
                new_google_drive_resource.url = google_drive_url
            else:
                new_google_drive_resource = Resource.objects.create(
                    friendly_name=google_drive_friendly_name,
                    folder=selected_event.folder,
                    url=google_drive_url,
                    icon=google_drive_icon
                )
            new_google_drive_resource.save()

            previous_is_public = selected_event.is_public
            
            selected_event.friendly_name = event_friendly_name
            selected_event.description = event_description
            selected_event.date = event_date
            selected_event.time = event_time
            selected_event.location = event_location
            selected_event.google_drive_link = new_google_drive_resource
            selected_event.register_link = new_register_resource
            selected_event.is_public = event_is_public
            selected_event.save()

            if (not previous_is_public) and event_is_public:
                new_event_notifications(selected_event.name)

            messages.success(request, 'Successfully edited event!')

            return redirect(reverse('events'))
    else:
        form = EventForm(instance=selected_event)

    register_link = selected_event.register_link
    if register_link:
        register_url = selected_event.register_link.url
        register_name = selected_event.register_link.name
    else:
        register_url = ''
        register_name = ''
    
    google_drive_link = selected_event.google_drive_link
    if google_drive_link:
        google_drive_url = selected_event.google_drive_link.url
        google_drive_name = selected_event.google_drive_link.name
    else:
        google_drive_url = ''
        google_drive_name = ''

    action_url = reverse('edit_event', args=(selected_event.name,))

    context = {
        'form': form,
        'selected_event': selected_event,
        'register_url': register_url,
        'register_name': register_name,
        'google_drive_url': google_drive_url,
        'google_drive_name': google_drive_name,
        'action_url': action_url,
        'page_heading': 'Edit',
        'delete_btn': True,
    }

    return render(request, 'events/event.html', context)


@login_required
def delete_event(request, event_name):

    user = request.user

    if not user.is_superuser:
        messages.error(request, "You must be an admin to delete an event!")
        return redirect(reverse('events'))
    
    selected_event = Event.objects.filter(name=event_name).first()

    if not selected_event:
        messages.error(request, "Invalid event!")
        return redirect(reverse('events'))
    
    selected_event.delete()

    messages.success(request, "Successfully deleted event!")
    return redirect(reverse('events'))


