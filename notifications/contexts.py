from .models import Notification


def notifications(request):
    all_notifications = None
    unread_important_notifications = None
    all_important_notifications = None
    unread_unimportant_notifications = None
    all_unimportant_notifications = None
    num_of_all_notifications = 0
    num_of_unread = 0
    
    user = request.user

    if user.is_authenticated:
        
        all_notifications = Notification.objects.filter(user=user, cleared_status=False).order_by('-date')

        num_of_all_notifications = all_notifications.count()

        all_important_notifications = all_notifications.filter(important_status=True)

        unread_important_notifications = all_important_notifications.filter(read_status=False)

        num_of_unread = unread_important_notifications.count()

        all_unimportant_notifications = all_notifications.filter(important_status=False)

        unread_unimportant_notifications = all_unimportant_notifications.filter(read_status=False)

    context = {
        'all_notifications': all_notifications,
        'num_of_all_notifications': num_of_all_notifications,
        'unread_important_notifications': unread_important_notifications,
        'all_important_notifications': all_important_notifications,
        'unread_unimportant_notifications': unread_unimportant_notifications,
        'all_unimportant_notifications': all_unimportant_notifications,
        'num_of_unread': num_of_unread,
    }
    return context