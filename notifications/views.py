from django.shortcuts import render, redirect, reverse
from .models import Notification
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from membership.models import Membership
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404
from notifications.contexts import get_notification_icon_html, get_age_string, get_url_name
from django.core.exceptions import ObjectDoesNotExist


@login_required
def view_notification(request, sku):
    user = request.user
    notification = get_object_or_404(Notification, sku=sku)

    if (notification.user != user) and (not user.is_superuser):
        messages.error(request, 'You must be the owner of this notification!')
        return redirect(reverse('home'))
    
    notification.cleared_status = True
    notification.icon = get_notification_icon_html(notification.category)
    notification.age = get_age_string(notification.date)
    notification.url_name = get_url_name(notification.category)
    notification.save()

    context = {
        'selected_notification': notification,
    }

    return render(request, 'notifications/view_notification.html', context)



@login_required
def delete_notification_from_view(request, sku):
    user = request.user
    notification = get_object_or_404(Notification, sku=sku)

    if (notification.user != user) and (not user.is_superuser):
        messages.error(request, 'You must be the owner of this notification!')
        return redirect(reverse('home'))
    
    notification.delete()

    messages.success(request, 'Successfully deleted notification!')

    return redirect(reverse('home'))
    

@login_required
def clear_all_notifications(request, username):
    user = request.user
    selected_user = User.objects.filter(username=username).first()

    if (selected_user != user) and (not user.is_superuser):
        messages.error(request, 'You must be the owner of these notifications!')
        return redirect(reverse('home'))

    notifications = Notification.objects.filter(user=user, cleared_status=False)

    if notifications.count() == 0:
        messages.info(request, 'No notifications to clear!')
        return redirect(request.META.get('HTTP_REFERER', 'home'))

    for notification in notifications:
        notification.cleared_status = True
        notification.save()

    message = 'Successfully cleared the notifications!'
    messages.success(request, message)

    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def delete_all_notifications(request, username):
    user = request.user
    selected_user = User.objects.filter(username=username).first()

    if (selected_user != user) and (not user.is_superuser):
        messages.error(request, 'You must be the owner of these notifications!')
        return redirect(request.META.get('HTTP_REFERER', 'home'))

    notifications = Notification.objects.filter(user=user, cleared_status=True)

    if notifications.count() == 0:
        messages.info(request, 'No notifications to delete!')
        return redirect(request.META.get('HTTP_REFERER', 'home'))

    for notification in notifications:
        notification.delete()

    message = 'Successfully deleted the notifications!'
    messages.success(request, message)

    return redirect(request.META.get('HTTP_REFERER', 'home'))
