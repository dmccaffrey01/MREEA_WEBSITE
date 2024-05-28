from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.utils import timezone
from membership.models import Membership
from .models import Annoucement
from resources.models import Resource, Folder
from django.contrib.auth.decorators import login_required


@login_required
def announcements(request):

    context = {
        
    }

    return render(request, 'announcements/announcements.html', context)
