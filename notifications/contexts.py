from .models import Notification
from django.shortcuts import reverse
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib import messages


def notifications(request):
    new_notifications = None
    cleared_notifications = None
    num_of_new_notifications = 0
    num_of_cleared_notifications = 0
    
    user = request.user

    if user.is_authenticated:
        current_time = timezone.now()

        # Filter notifications with date in the past or today and cleared status as False
        new_notifications = Notification.objects.filter(
            user=user, 
            cleared_status=False, 
            date__lte=current_time
        ).order_by('-date')
        num_of_new_notifications = new_notifications.count()

        # Filter cleared notifications with date in the past or today
        cleared_notifications = Notification.objects.filter(
            user=user,
            cleared_status=True,
            date__lte=current_time
        ).order_by('-date')
        num_of_cleared_notifications = cleared_notifications.count()

        # Assign icon class and age for new notifications
        for n in new_notifications:
            n.age = get_age_string(n.date)
            n.icon = get_notification_icon_html(n.category)
            n.url_name = get_url_name(n.category)

        # Assign icon class and age for cleared notifications
        for n in cleared_notifications:
            n.age = get_age_string(n.date)
            n.icon = get_notification_icon_html(n.category)
            n.url_name = get_url_name(n.category)
            
    context = {
        'new_notifications': new_notifications,
        'cleared_notifications': cleared_notifications,
        'num_of_new_notifications': num_of_new_notifications,
        'num_of_cleared_notifications': num_of_cleared_notifications,
    }
    return context


def get_url_name(category):
    if category == 'membership':
        url_name = 'Membership'
    else:
        url_name = 'Link'
    
    return url_name


def get_notification_icon_html(category):
    if category == 'membership':
        html = """
        <svg xmlns="http://www.w3.org/2000/svg" class="dark-text" viewBox="0 0 24 24">
            <path fill-rule="evenodd" d="M10.193 9.556L12 6.665l1.807 2.891a.85.85 0 0 0 1.221.237l3.88-2.822l-1.49 7.826a.25.25 0 0 1-.245.203H6.828a.25.25 0 0 1-.246-.203L5.092 6.97l3.88 2.822a.85.85 0 0 0 1.22-.237m2.528-4.568a.85.85 0 0 0-1.442 0L9.29 8.17L4.646 4.792c-.623-.453-1.48.09-1.335.846l1.797 9.44a1.75 1.75 0 0 0 1.72 1.422h10.345a1.75 1.75 0 0 0 1.719-1.423l1.797-9.439c.145-.756-.711-1.3-1.334-.846L14.71 8.17zM6 18a.75.75 0 0 0 0 1.5h12a.75.75 0 1 0 0-1.5z" clip-rule="evenodd" />
        </svg>
        """
    elif category == 'events':
        html = """
        <svg xmlns="http://www.w3.org/2000/svg" class="dark-text" viewBox="0 0 16 16">
            <path d="M5.248 8.997a.748.748 0 1 0 0-1.497a.748.748 0 0 0 0 1.497m.749 1.752a.748.748 0 1 1-1.497 0a.748.748 0 0 1 1.497 0M8 8.997A.748.748 0 1 0 8 7.5a.748.748 0 0 0 0 1.497m.749 1.752a.748.748 0 1 1-1.497 0a.748.748 0 0 1 1.497 0m2-1.752a.748.748 0 1 0 0-1.497a.748.748 0 0 0 0 1.497M14 4.5A2.5 2.5 0 0 0 11.5 2h-7A2.5 2.5 0 0 0 2 4.5v7A2.5 2.5 0 0 0 4.5 14h7a2.5 2.5 0 0 0 2.5-2.5zM3 6h10v5.5a1.5 1.5 0 0 1-1.5 1.5h-7A1.5 1.5 0 0 1 3 11.5zm1.5-3h7A1.5 1.5 0 0 1 13 4.5V5H3v-.5A1.5 1.5 0 0 1 4.5 3" />
        </svg>
        """
    else:
        html = """
        <svg xmlns="http://www.w3.org/2000/svg" class="dark-text" viewBox="0 0 256 256">
            <path d="M168 224a8 8 0 0 1-8 8H96a8 8 0 1 1 0-16h64a8 8 0 0 1 8 8m53.85-32a15.8 15.8 0 0 1-13.85 8H48a16 16 0 0 1-13.8-24.06C39.75 166.38 48 139.34 48 104a80 80 0 1 1 160 0c0 35.33 8.26 62.38 13.81 71.94a15.89 15.89 0 0 1 .03 16.06ZM208 184c-7.73-13.27-16-43.95-16-80a64 64 0 1 0-128 0c0 36.06-8.28 66.74-16 80Z" />
        </svg>
        """
    return html


def get_age_string(date):
    today = timezone.now()  # Get the current datetime
    date = date  # Assume `date` is already a datetime object

    # Check if the notification occurred today
    if date.date() == today.date():
        time_diff = today - date
        seconds_diff = time_diff.total_seconds()
        if seconds_diff < 60:
            return f"{int(seconds_diff)}s"  # Display seconds
        elif seconds_diff < 3600:
            return f"{int(seconds_diff/60)}m"  # Display minutes
        else:
            return f"{int(seconds_diff/3600)}h"  # Display hours
    else:
        days_diff = (today.date() - date.date()).days
        return f"{days_diff}d"  # Display days
