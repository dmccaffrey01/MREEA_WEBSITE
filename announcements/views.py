from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.utils import timezone
from datetime import timedelta
from membership.models import Membership
from .models import Announcement
from resources.models import Resource, Folder, Icon
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AnnouncementForm
from .tasks import new_announcement_notifications


@login_required
def announcements(request):

    user = request.user

    membership = Membership.objects.filter(user=user).first()

    if not membership:
        messages.error(request, "You must be a member to access this!")
        return redirect(reverse('membership_redirect'))

    if not membership:
        messages.error(request, "You memberhip must be valid to access this!")
        return redirect(reverse('membership_redirect'))

    all_announcements = Announcement.objects.all()

    public_announcements = all_announcements.filter(is_public=True)

    today = timezone.localtime(timezone.now())
    tomorrow = today + timedelta(days=1)
    torrow_start = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
    one_month_ago = torrow_start - timedelta(days=30)

    recent_announcements_query = public_announcements.filter(date_made_public__gte=one_month_ago).order_by('-date_made_public')
    past_announcements_query = public_announcements.filter(date_made_public__lt=one_month_ago).order_by('-date_made_public')

    if request.method == 'POST':
        viewAllValue = request.POST.get('id_view_all')

        if viewAllValue == 'recent':
            recent_slice = recent_announcements_query.count()
            past_slice = 4
        else:
            past_slice = past_announcements_query.count()
            recent_slice = 4
    else:
        recent_slice = 4
        past_slice = 4

    draft_announcements = all_announcements.filter(is_public=False)
    recent_announcements = recent_announcements_query[:recent_slice]
    past_announcements = past_announcements_query[:past_slice]

    context = {
        'recent_announcements': recent_announcements,
        'past_announcements': past_announcements,
        'draft_announcements': draft_announcements,
    }

    return render(request, 'announcements/announcements.html', context)


@login_required
def add_announcement(request):

    user = request.user

    if not user.is_superuser:
        messages.error(request, "You must be an admin to add an announcement!")
        return redirect(reverse('announcements'))
    
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)

        if form.is_valid():
            form_data = form.cleaned_data
            announcement_friendly_name = form_data['friendly_name']
            announcement_description = form_data['description']
            announcement_is_public = form_data['is_public']

            announcements_parent_folder = Folder.objects.filter(name='announcements').first()
            folder_icon = Icon.objects.filter(name='folder').first()
            new_folder, created = Folder.objects.get_or_create(
                friendly_name=announcement_friendly_name,
                parent_folder=announcements_parent_folder,
                icon=folder_icon
            )
            new_folder.save()

            new_announcement = Announcement.objects.create(
                friendly_name=announcement_friendly_name,
                description=announcement_description,
                folder=new_folder,
                is_public=announcement_is_public,
            )

            print(new_folder)

            new_announcement.save()

            if announcement_is_public:
                new_announcement.date_made_public = timezone.localtime(timezone.now())
                new_announcement.save()
                # new_announcement_notifications.delay(new_announcement.name) # celery task

            messages.success(request, 'Successfully created announcement!')

            return redirect(reverse('announcements'))
    else:
        form = AnnouncementForm()

    action_url = reverse('add_announcement')

    context = {
        'form': form,
        'register_url': '',
        'google_drive_url': '',
        'action_url': action_url,
        'page_heading': 'Add',
    }

    return render(request, 'announcements/announcement.html', context)


@login_required
def edit_announcement(request, announcement_name):

    user = request.user

    if not user.is_superuser:
        messages.error(request, "You must be an admin to edit an announcement!")
        return redirect(reverse('announcements'))
    
    selected_announcement = Announcement.objects.filter(name=announcement_name).first()

    if not selected_announcement:
        messages.error(request, "Invalid announcement!")
        return redirect(reverse('announcements'))
    
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)

        if form.is_valid():
            form_data = form.cleaned_data
            announcement_friendly_name = form_data['friendly_name']
            announcement_description = form_data['description']
            announcement_is_public = form_data['is_public']
            previous_is_public = selected_announcement.is_public
            
            selected_announcement.friendly_name = announcement_friendly_name
            selected_announcement.description = announcement_description
            selected_announcement.is_public = announcement_is_public
            selected_announcement.save()

            if (not previous_is_public) and announcement_is_public:
                selected_announcement.date_made_public = timezone.localtime(timezone.now())
                selected_announcement.save()
                # new_announcement_notifications.delay(selected_announcement.name) # celery task

            messages.success(request, 'Successfully edited announcement!')

            return redirect(reverse('announcements'))
    else:
        form = AnnouncementForm(instance=selected_announcement)

    action_url = reverse('edit_announcement', args=(selected_announcement.name,))

    context = {
        'form': form,
        'selected_announcement': selected_announcement,
        'action_url': action_url,
        'page_heading': 'Edit',
        'delete_btn': True,
    }

    return render(request, 'announcements/announcement.html', context)


@login_required
def delete_announcement(request, announcement_name):

    user = request.user

    if not user.is_superuser:
        messages.error(request, "You must be an admin to delete an announcement!")
        return redirect(reverse('announcements'))
    
    selected_announcement = Announcement.objects.filter(name=announcement_name).first()

    if not selected_announcement:
        messages.error(request, "Invalid announcement!")
        return redirect(reverse('announcements'))
    
    selected_announcement.delete()

    messages.success(request, "Successfully deleted announcement!")
    return redirect(reverse('announcements'))
