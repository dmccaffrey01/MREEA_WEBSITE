from .models import Notification
from django.shortcuts import reverse


def notifications(request):
    notifications = None
    cleared_notifications = None
    num_of_notifications = 0
    num_of_cleared_notifications = 0
    
    user = request.user

    if user.is_authenticated:
        notifications = Notification.objects.filter(user=user, cleared_status=False).order_by('-date')
        num_of_notifications = notifications.count()

        cleared_notifications = Notification.objects.filter(cleared_status=True).order_by('-date')
        num_of_cleared_notifications = cleared_notifications.count()

        for n in notifications:
            n.icon_class = get_icon_class_for_category(n.category)

        for n in cleared_notifications:
            n.icon_class = get_icon_class_for_category(n.category)
            
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