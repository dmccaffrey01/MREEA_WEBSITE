from .models import Notification
from django.shortcuts import reverse
from datetime import datetime, timedelta
from django.utils import timezone


def notifications(request):
    notifications = None
    cleared_notifications = None
    num_of_notifications = 0
    num_of_cleared_notifications = 0
    
    user = request.user

    if user.is_authenticated:
        current_time = timezone.now()

        # Filter notifications with date in the past or today and cleared status as False
        notifications = Notification.objects.filter(
            user=user, 
            cleared_status=False, 
            date__lte=current_time
        ).order_by('-date')
        num_of_notifications = notifications.count()

        # Filter cleared notifications with date in the past or today
        cleared_notifications = Notification.objects.filter(
            cleared_status=True,
            date__lte=current_time
        ).order_by('-date')
        num_of_cleared_notifications = cleared_notifications.count()

        # Assign icon class and age for notifications
        for n in notifications:
            n.icon_class = get_icon_class_for_category(n.category)
            n.age = get_age_string(n.date)

        # Assign icon class and age for cleared notifications
        for n in cleared_notifications:
            n.icon_class = get_icon_class_for_category(n.category)
            n.age = get_age_string(n.date)
            
    context = {
        'notifications': notifications,
        'cleared_notifications': cleared_notifications,
        'num_of_notifications': num_of_notifications,
        'num_of_cleared_notifications': num_of_cleared_notifications,
    }
    return context

def get_icon_class_for_category(category):
    if category == 'membership':
        return 'fa-solid fa-crown'
    elif category == 'events':
        return 'fa-solid fa-calendar-day'
    elif category == 'announcements':
        return 'fa-solid fa-bullhorn'
    elif category == 'resources':
        return 'fa-solid fa-layer-group'
    elif category == 'members':
        return 'fa-solid fa-users'
    elif category == 'testimonials':
        return 'fa-solid fa-comments'
    elif category == 'blog':
        return 'fa-solid fa-file-pen'
    elif category == 'contact':
        return 'fa-solid fa-envelope'
    else:
        return 'fa-solid fa-circle-info'
    

def get_age_string(date):
    today = timezone.now().date()  # Get the current date
    date = date.date()  # Extract the date part from the datetime object

    days_diff = (today - date).days
    return f"{days_diff}d"