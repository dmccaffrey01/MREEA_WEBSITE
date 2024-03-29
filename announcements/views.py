from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.utils import timezone
from membership.models import Membership
from .models import Annoucement
from resources.models import Resource, Folder
from django.contrib.auth.decorators import login_required


@login_required
def announcements(request):

    user = request.user

    membership = Membership.objects.get(user=user)

    if membership:
        if not (membership.status.valid or user.is_superuser):
            return redirect(reverse('membership'))
    else:
        return redirect(reverse('membership'))
    
    current_datetime = timezone.now()
    
    announcements = Folder.objects.filter(date__lt=current_datetime).order_by('-date')

    context = {
        'announcements': announcements,
    }

    return render(request, 'announcements/announcements.html', context)


def announcement_detail(request, announcement_name):
    # event = get_object_or_404(Event, name=event_name)

    # user = request.user
    
    # membership = Membership.objects.get(user=user)

    # if membership.status.valid:
    #     display_folder = True
    #     folders = Folder.objects.filter(parent_folder=event.folder)
    #     resources = Resource.objects.filter(folder=event.folder)
    # else:
    #     display_folder = False
    #     folders = False
    #     resources = False

    # context = {
    #     'event': event,
    #     'display_folder': display_folder,
    #     'folders': folders,
    #     'resources': resources,
    # }

    return render(request, 'events/event_detail.html', context)