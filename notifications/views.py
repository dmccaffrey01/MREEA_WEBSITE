from django.shortcuts import render, redirect, reverse
from .models import Notification
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from membership.models import Membership
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404


def notifications(request):

    context = {

    }

    return render(request, 'notifications/notifications.html', context)


def get_messages(request):
    # Get messages from Django messages framework
    django_messages = messages.get_messages(request)

    # Convert messages to a list of dictionaries
    messages_list = [{'message': message.message, 'tags': message.tags} for message in django_messages]

    return JsonResponse({'messages': messages_list})

@login_required
def handle_notification(request, notification_data):
    category = notification_data['category']

    notification_type = notification_data['notification_type']

    notify_admins = notification_data['notify_admins']

    if category == 'membership':
        handle_membership_notification(request,category,  notification_type, notify_admins)
    # elif category == 'events':
    #     handle_events_notification(request, category, notification_type, notify_admins)
    # elif category == 'events':
    #     handle_events_notification(request, category, notification_type, notify_admins)
    # elif category == 'events':
    #     handle_events_notification(request, category, notification_type, notify_admins)
    # elif category == 'events':
    #     handle_events_notification(request, category, notification_type, notify_admins)


def handle_membership_notification(request, category, notification_type, notify_admins):
    user = request.user

    users_to_notify = []

    users_to_notify.append(user)

    if notify_admins:
        admins = User.objects.filter(is_superuser=True)
        for admin in admins:
            users_to_notify.append(admin)

    for user in users_to_notify:
        if notification_type == 'pending':
            heading = 'Membership Pending Approval!'

            if user.is_superuser:
                message = f"{user.first_name} {user.last_name}'s ({user.email}) membership is pending. Please check their payment and then approve or deny their membership."
                url = reverse('user_admin')
            else:
                message = 'We have received your pending membership, once we have confirmed payment we will update your membership and you will be notified. Thank you for you patience,'
                url = reverse('membership_status')

        notification = Notification.objects.create(
            user=user,
            heading=heading,
            message=message,
            category=category,
            url=url,
        )
        notification.save()
        

@login_required
def clear_notification(request, sku):
    try:
        notification = get_object_or_404(Notification, sku=sku)

        if notification.user != request.user:
            raise ValueError('You must be the owner of the notification to clear it.')

        notification.cleared_status = True
        notification.save()

        message = 'Successfully cleared the notification!'
        messages.success(request, message)

        return JsonResponse({'success': True, 'message': message})

    except Notification.DoesNotExist:
        message = 'Invalid Notification'
        messages.error(request, message)
        return JsonResponse({'success': False, 'message': message})

    except ValueError as e:
        message = f'Unsuccessfully cleared the notification! - {e}'
        messages.error(request, message)
        return JsonResponse({'success': False, 'message': message})

    except Exception as e:
        message = f'An error occurred: {e}'
        messages.error(request, message)
        return JsonResponse({'success': False, 'message': message})
        

@login_required
def delete_notification(request, sku):
    try:
        notification = get_object_or_404(Notification, sku=sku)

        if notification.user != request.user:
            raise ValueError('You must be the owner of the notification to delete it.')

        notification.delete()

        message = 'Successfully deleted the notification!'
        messages.success(request, message)

        return JsonResponse({'success': True, 'message': message})

    except Notification.DoesNotExist:
        message = 'Invalid Notification'
        messages.error(request, message)
        return JsonResponse({'success': False, 'message': message})

    except ValueError as e:
        message = f'Unsuccessfully deleted the notification! - {e}'
        messages.error(request, message)
        return JsonResponse({'success': False, 'message': message})

    except Exception as e:
        message = f'An error occurred: {e}'
        messages.error(request, message)
        return JsonResponse({'success': False, 'message': message})
        
