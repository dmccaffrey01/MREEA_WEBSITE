from .models import Notification
from django.shortcuts import reverse
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib import messages


def custom_messages(request):
    # Get messages from Django messages framework
    django_messages = messages.get_messages(request)

    if not django_messages:
        return {}
    
    messages_list = []

    for message in django_messages:
        message_icon_html = get_message_icon_html(message.tags)
        m = {
            'message': message.message,
            'tags': message.tags,
            'icon': message_icon_html
        }
        messages_list.append(m)

    return ({'custom_messages': messages_list})


def get_message_icon_html(tags):
    if tags == 'success':
        html = """
        <svg xmlns="http://www.w3.org/2000/svg" class="white-text" viewBox="0 0 24 24">
            <path fill-rule="evenodd" d="M20.207 6.793a1 1 0 0 1 0 1.414l-9.5 9.5a1 1 0 0 1-1.414 0l-4.5-4.5a1 1 0 0 1 1.414-1.414L10 15.586l8.793-8.793a1 1 0 0 1 1.414 0" clip-rule="evenodd" />
        </svg>
        """
    elif tags == 'error':
        html = """
        <svg xmlns="http://www.w3.org/2000/svg" class="white-text" viewBox="0 0 24 24">
            <path fill-rule="evenodd" d="M17.707 7.707a1 1 0 0 0-1.414-1.414L12 10.586L7.707 6.293a1 1 0 0 0-1.414 1.414L10.586 12l-4.293 4.293a1 1 0 1 0 1.414 1.414L12 13.414l4.293 4.293a1 1 0 1 0 1.414-1.414L13.414 12z" clip-rule="evenodd" />
        </svg>
        """
    elif tags == 'warning':
        html = """
        <svg xmlns="http://www.w3.org/2000/svg" class="white-text" viewBox="0 0 24 24">
            <path fill-rule="evenodd" d="M11.001 15.046a1 1 0 0 0 1.998 0l.477-10.501a1.478 1.478 0 1 0-2.952 0zM12 18a1.5 1.5 0 0 0-1.5 1.5v.01a1.5 1.5 0 0 0 1.5 1.5h.01a1.5 1.5 0 0 0 1.5-1.5v-.01a1.5 1.5 0 0 0-1.5-1.5z" clip-rule="evenodd" />
        </svg>
        """
    else:
        html = """
        <svg xmlns="http://www.w3.org/2000/svg" class="white-text" viewBox="0 0 56 56">
            <path d="M24.332 13.246c0 1.875 1.5 3.375 3.375 3.375c1.898 0 3.375-1.5 3.352-3.375c0-1.898-1.454-3.398-3.352-3.398c-1.875 0-3.375 1.5-3.375 3.398M18.52 44.231c0 1.148.82 1.921 2.062 1.921h14.836c1.242 0 2.063-.773 2.063-1.922c0-1.124-.82-1.898-2.063-1.898h-4.711V24.449c0-1.265-.82-2.11-2.039-2.11h-7.43c-1.218 0-2.039.75-2.039 1.876c0 1.172.82 1.945 2.04 1.945h5.132v16.172h-5.789c-1.242 0-2.062.773-2.062 1.898" />
        </svg>
        """
    return html

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
        <svg xmlns="http://www.w3.org/2000/svg" class="dark-text-2" viewBox="0 0 24 24">
            <path fill-rule="evenodd" d="M10.193 9.556L12 6.665l1.807 2.891a.85.85 0 0 0 1.221.237l3.88-2.822l-1.49 7.826a.25.25 0 0 1-.245.203H6.828a.25.25 0 0 1-.246-.203L5.092 6.97l3.88 2.822a.85.85 0 0 0 1.22-.237m2.528-4.568a.85.85 0 0 0-1.442 0L9.29 8.17L4.646 4.792c-.623-.453-1.48.09-1.335.846l1.797 9.44a1.75 1.75 0 0 0 1.72 1.422h10.345a1.75 1.75 0 0 0 1.719-1.423l1.797-9.439c.145-.756-.711-1.3-1.334-.846L14.71 8.17zM6 18a.75.75 0 0 0 0 1.5h12a.75.75 0 1 0 0-1.5z" clip-rule="evenodd" />
        </svg>
        """
    elif category == 'events':
        html = """
        <svg xmlns="http://www.w3.org/2000/svg" class="dark-text-2" viewBox="0 0 16 16">
            <path d="M5.248 8.997a.748.748 0 1 0 0-1.497a.748.748 0 0 0 0 1.497m.749 1.752a.748.748 0 1 1-1.497 0a.748.748 0 0 1 1.497 0M8 8.997A.748.748 0 1 0 8 7.5a.748.748 0 0 0 0 1.497m.749 1.752a.748.748 0 1 1-1.497 0a.748.748 0 0 1 1.497 0m2-1.752a.748.748 0 1 0 0-1.497a.748.748 0 0 0 0 1.497M14 4.5A2.5 2.5 0 0 0 11.5 2h-7A2.5 2.5 0 0 0 2 4.5v7A2.5 2.5 0 0 0 4.5 14h7a2.5 2.5 0 0 0 2.5-2.5zM3 6h10v5.5a1.5 1.5 0 0 1-1.5 1.5h-7A1.5 1.5 0 0 1 3 11.5zm1.5-3h7A1.5 1.5 0 0 1 13 4.5V5H3v-.5A1.5 1.5 0 0 1 4.5 3" />
        </svg>
        """
    elif category == 'announcements':
        html = """
        <svg xmlns="http://www.w3.org/2000/svg" class="dark-text-2" viewBox="0 0 24 24">
            <path fill-rule="evenodd" d="M20.085 16.932a62.152 62.152 0 0 0 0-12.864c-.159-1.525-1.917-2.298-3.148-1.383l-4.103 3.05a7.25 7.25 0 0 1-4.326 1.432H4.68c-.69 0-1.25.56-1.25 1.25v4.166c0 .69.56 1.25 1.25 1.25h.624l-.845 3.155a.75.75 0 0 0 .408.874l3.68 1.717a.75.75 0 0 0 1.042-.486l1.263-4.712a.78.78 0 0 0 .024-.15a7.25 7.25 0 0 1 1.959 1.034l4.103 3.05c1.23.915 2.99.142 3.148-1.383m-1.492-12.71a60.696 60.696 0 0 1 0 12.555a.478.478 0 0 1-.76.334l-4.105-3.05a8.75 8.75 0 0 0-5.22-1.728H4.93V8.667h3.58a8.75 8.75 0 0 0 5.22-1.728l4.103-3.05a.478.478 0 0 1 .76.334m-9.157 9.67a7.256 7.256 0 0 0-.928-.059H6.856L6.07 16.77l2.3 1.073l1.032-3.85a.759.759 0 0 1 .034-.1" clip-rule="evenodd" />
        </svg>
        """
    elif category == 'testimonials':
        html = """
        <svg xmlns="http://www.w3.org/2000/svg" class="dark-text-2" viewBox="0 0 16 16">
            <path d="M11 4a1 1 0 1 1 0 2a1 1 0 0 1 0-2m.885 2.794c-.23 1.592-.852 2.966-2.239 4.352a.5.5 0 0 0 .708.708C12.473 9.734 13 7.592 13 5a2 2 0 1 0-1.115 1.794M5 4a1 1 0 1 1 0 2a1 1 0 0 1 0-2m.885 2.794c-.23 1.592-.852 2.966-2.239 4.352a.5.5 0 0 0 .708.708C6.473 9.734 7 7.592 7 5a2 2 0 1 0-1.115 1.794" />
        </svg>
        """
    elif category == 'password':
        html = """
        <svg xmlns="http://www.w3.org/2000/svg" class="dark-text-2" viewBox="0 0 16 16">
            <path d="M9 9a1 1 0 1 1-2 0a1 1 0 0 1 2 0M5 4h-.5A2.5 2.5 0 0 0 2 6.5v5A2.5 2.5 0 0 0 4.5 14h7a2.5 2.5 0 0 0 2.5-2.5v-5A2.5 2.5 0 0 0 11.5 4H11v-.5a3 3 0 0 0-6 0zm1-.5a2 2 0 1 1 4 0V4H6zM11.5 5A1.5 1.5 0 0 1 13 6.5v5a1.5 1.5 0 0 1-1.5 1.5h-7A1.5 1.5 0 0 1 3 11.5v-5A1.5 1.5 0 0 1 4.5 5z" />
        </svg>
        """
    else:
        html = """
        <svg xmlns="http://www.w3.org/2000/svg" class="dark-text-2" viewBox="0 0 256 256">
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
