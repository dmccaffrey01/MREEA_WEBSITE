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
            <path d="M21.56 4.607a1.81 1.81 0 0 0-2-.54a1.75 1.75 0 0 0-.79.63l-2.56 2.48l-2.66-3.64a1.769 1.769 0 0 0-2.48-.65a1.76 1.76 0 0 0-.62.65l-2.66 3.64l-2.56-2.48a1.77 1.77 0 0 0-2.84-.09A1.76 1.76 0 0 0 2 5.687v9.8a5.89 5.89 0 0 0 5.89 5.89h8.22a5.91 5.91 0 0 0 5.89-5.89v-9.83a1.83 1.83 0 0 0-.44-1.05m-5.57 12.91h-8a1 1 0 0 1 0-2h8a1 1 0 1 1 0 2" />
        </svg>
        """
    elif category == 'events':
        html = """
        <svg xmlns="http://www.w3.org/2000/svg" class="dark-text" viewBox="0 0 24 24">
            <path d="M7.75 2.5a.75.75 0 0 0-1.5 0v1.58c-1.44.115-2.384.397-3.078 1.092c-.695.694-.977 1.639-1.093 3.078h19.842c-.116-1.44-.398-2.384-1.093-3.078c-.694-.695-1.639-.977-3.078-1.093V2.5a.75.75 0 0 0-1.5 0v1.513C15.585 4 14.839 4 14 4h-4c-.839 0-1.585 0-2.25.013z" />
            <path fill-rule="evenodd" d="M22 12v2c0 3.771 0 5.657-1.172 6.828C19.657 22 17.771 22 14 22h-4c-3.771 0-5.657 0-6.828-1.172C2 19.657 2 17.771 2 14v-2c0-.839 0-1.585.013-2.25h19.974C22 10.415 22 11.161 22 12m-5.5 6a1.5 1.5 0 1 0 0-3a1.5 1.5 0 0 0 0 3" clip-rule="evenodd" />
        </svg>
        """
    else:
        html = """
        <svg xmlns="http://www.w3.org/2000/svg" class="dark-text" viewBox="0 0 24 24">
            <path d="M12 2a7 7 0 0 0-7 7v3.528a1 1 0 0 1-.105.447l-1.717 3.433A1.1 1.1 0 0 0 4.162 18h15.676a1.1 1.1 0 0 0 .984-1.592l-1.716-3.433a1 1 0 0 1-.106-.447V9a7 7 0 0 0-7-7m0 19a3.001 3.001 0 0 1-2.83-2h5.66A3.001 3.001 0 0 1 12 21" />
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
