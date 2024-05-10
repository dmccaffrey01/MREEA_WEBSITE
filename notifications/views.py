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


def view_notification(request, sku):
    user = request.user
    try:
        notification = Notification.objects.filter(sku=sku).first()

        if not notification:
            raise ObjectDoesNotExist('Notification does not exist')

        if (notification.user != user) and (not user.is_superuser):
            raise ValueError('You must be the owner of the notification to view it.')
        
        notification.cleared_status = True
        notification.icon = get_notification_icon_html(notification.category)
        notification.age = get_age_string(notification.date)
        notification.url_name = get_url_name(notification.category)
        notification.save()

        message = f'Viewing Notification!'
        messages.info(request, message)

        context = {
            'selected_notification': notification,
        }

        return render(request, 'notifications/view_notification.html', context)

    except ObjectDoesNotExist as e:
        message = str(e)
        messages.error(request, message)
        return redirect(reverse('home'))

    except ValueError as e:
        message = f'Unsuccessfully viewed the notification! - {e}'
        messages.error(request, message)
        return redirect(reverse('home'))

    except Exception as e:
        message = f'An error occurred: {e}'
        messages.error(request, message)
        return redirect(reverse('home'))


def get_messages(request):
    # Get messages from Django messages framework
    django_messages = messages.get_messages(request)
    messages_list = []

    for message in django_messages:
        message_icon_html = get_message_icon_html(message.tags)
        m = {
            'message': message.message,
            'tags': message.tags,
            'icon': message_icon_html
        }
        messages_list.append(m)

    return JsonResponse({'messages': messages_list})


def get_message_icon_html(tags):
    if tags == 'success':
        html = """
        <svg xmlns="http://www.w3.org/2000/svg" class="dark-text color-success" viewBox="0 0 24 24">
            <g fill-rule="evenodd">
                <path d="M21.546 5.111a1.5 1.5 0 0 1 0 2.121L10.303 18.475a1.6 1.6 0 0 1-2.263 0L2.454 12.89a1.5 1.5 0 1 1 2.121-2.121l4.596 4.596L19.424 5.111a1.5 1.5 0 0 1 2.122 0" />
            </g>
        </svg>
        """
    elif tags == 'error':
        html = """
        <svg xmlns="http://www.w3.org/2000/svg" class="dark-text color-error" viewBox="0 0 15 15">
            <path d="M3.64 2.27L7.5 6.13l3.84-3.84A.92.92 0 0 1 12 2a1 1 0 0 1 1 1a.9.9 0 0 1-.27.66L8.84 7.5l3.89 3.89A.9.9 0 0 1 13 12a1 1 0 0 1-1 1a.92.92 0 0 1-.69-.27L7.5 8.87l-3.85 3.85A.92.92 0 0 1 3 13a1 1 0 0 1-1-1a.9.9 0 0 1 .27-.66L6.16 7.5L2.27 3.61A.9.9 0 0 1 2 3a1 1 0 0 1 1-1c.24.003.47.1.64.27" />
        </svg>
        """
    elif tags == 'warning':
        html = """
        <svg xmlns="http://www.w3.org/2000/svg" class="dark-text color-warning" viewBox="0 0 192 512">
            <path d="M176 432c0 44.112-35.888 80-80 80s-80-35.888-80-80s35.888-80 80-80s80 35.888 80 80M25.26 25.199l13.6 272C39.499 309.972 50.041 320 62.83 320h66.34c12.789 0 23.331-10.028 23.97-22.801l13.6-272C167.425 11.49 156.496 0 142.77 0H49.23C35.504 0 24.575 11.49 25.26 25.199" />
        </svg>
        """
    else:
        html = """
        <svg xmlns="http://www.w3.org/2000/svg" class="dark-text color-info" viewBox="0 0 36 36">
            <circle cx="20.75" cy="6" r="4" class="clr-i-solid clr-i-solid-path-1" />
            <path d="M24.84 26.23a1 1 0 0 0-1.4.29a16.6 16.6 0 0 1-3.51 3.77c-.33.25-1.56 1.2-2.08 1c-.36-.11-.15-.82-.08-1.12l.53-1.57c.22-.64 4.05-12 4.47-13.3c.62-1.9.35-3.77-2.48-3.32c-.77.08-8.58 1.09-8.72 1.1a1 1 0 0 0 .13 2s3-.39 3.33-.42a.88.88 0 0 1 .85.44a2.47 2.47 0 0 1-.07 1.71c-.26 1-4.37 12.58-4.5 13.25a2.78 2.78 0 0 0 1.18 3a5 5 0 0 0 3.08.83a8.53 8.53 0 0 0 3.09-.62c2.49-1 5.09-3.66 6.46-5.75a1 1 0 0 0-.28-1.29" class="clr-i-solid clr-i-solid-path-2" />
        </svg>
        """
    return html


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
                message = 'We have received your pending membership, once we have confirmed payment we will update your membership and you will be notified. Thank you for you patience!'
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
def visit_url_notification(request, sku):
    user = request.user
    try:
        notification = Notification.objects.filter(sku=sku).first()

        if not notification:
            raise ObjectDoesNotExist('Notification does not exist')

        if (notification.user != user) and (not user.is_superuser):
            raise ValueError('You must be the owner of the notification to redirect to it\'s link.')

        notification.cleared_status = True
        notification_url_name = get_url_name(notification.category)
        notification.save()

        message = f'Redirecting to {notification_url_name}!'
        messages.success(request, message)

        return JsonResponse({'success': True, 'message': message, 'url': notification.url})

    except ObjectDoesNotExist as e:
        message = str(e)
        messages.error(request, message)
        return JsonResponse({'success': False, 'message': message})

    except ValueError as e:
        message = f'Unsuccessfully redirected to the notification\s link! - {e}'
        messages.error(request, message)
        return JsonResponse({'success': False, 'message': message})

    except Exception as e:
        message = f'An error occurred: {e}'
        messages.error(request, message)
        return JsonResponse({'success': False, 'message': message})


@login_required
def clear_notification(request, sku):
    user = request.user
    try:
        notification = Notification.objects.filter(sku=sku).first()

        if not notification:
            raise ObjectDoesNotExist('Notification does not exist')

        if (notification.user != user) and (not user.is_superuser):
            raise ValueError('You must be the owner of the notification to clear it.')

        notification.cleared_status = True
        notification.save()

        message = 'Successfully cleared the notification!'
        messages.success(request, message)

        return JsonResponse({'success': True, 'message': message})

    except ObjectDoesNotExist as e:
        message = str(e)
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
def unclear_notification(request, sku):
    user = request.user

    try:
        notification = Notification.objects.filter(sku=sku).first()

        if not notification:
            raise ObjectDoesNotExist('Notification does not exist')

        if (notification.user != user) and (not user.is_superuser):
            raise ValueError('You must be the owner of the notification to clear it.')

        notification.cleared_status = False
        notification.save()

        message = 'Successfully uncleared the notification!'
        messages.success(request, message)

        return JsonResponse({'success': True, 'message': message})

    except ObjectDoesNotExist as e:
        message = str(e)
        messages.error(request, message)
        return JsonResponse({'success': False, 'message': message})

    except ValueError as e:
        message = f'Unsuccessfully uncleared the notification! - {e}'
        messages.error(request, message)
        return JsonResponse({'success': False, 'message': message})

    except Exception as e:
        message = f'An error occurred: {e}'
        messages.error(request, message)
        return JsonResponse({'success': False, 'message': message})


@login_required
def clear_all_notifications(request, username):
    user = request.user
    try:
        user = request.user
        selected_user = User.objects.filter(username=username).first()

        if (selected_user != user) and (not user.is_superuser):
            raise ValueError('You must be the owner of these notifications to clear them.')

        notifications = Notification.objects.filter(user=user, cleared_status=False)

        notification_skus = []

        for notification in notifications:
            notification.cleared_status = True
            notification.save()
            notification_skus.append(notification.sku)

        message = 'Successfully cleared the notifications!'
        messages.success(request, message)

        return JsonResponse({'success': True, 'message': message, 'skus': notification_skus})

    except Notification.DoesNotExist:
        message = 'Invalid Notification'
        messages.error(request, message)
        return JsonResponse({'success': False, 'message': message})

    except ValueError as e:
        message = f'Unsuccessfully cleared the notifications! - {e}'
        messages.error(request, message)
        return JsonResponse({'success': False, 'message': message})

    except Exception as e:
        message = f'An error occurred: {e}'
        messages.error(request, message)
        return JsonResponse({'success': False, 'message': message})


@login_required
def unclear_all_notifications(request, username):
    user = request.user
    try:
        user = request.user
        selected_user = User.objects.filter(username=username).first()

        if (selected_user != user) and (not user.is_superuser):
            raise ValueError('You must be the owner of these notifications to unclear them.')

        notifications = Notification.objects.filter(user=user, cleared_status=True)

        notification_skus = []

        for notification in notifications:
            notification.cleared_status = False
            notification.save()
            notification_skus.append(notification.sku)

        message = 'Successfully uncleared the notifications!'
        messages.success(request, message)

        return JsonResponse({'success': True, 'message': message, 'skus': notification_skus})

    except Notification.DoesNotExist:
        message = 'Invalid Notification'
        messages.error(request, message)
        return JsonResponse({'success': False, 'message': message})

    except ValueError as e:
        message = f'Unsuccessfully uncleared the notifications! - {e}'
        messages.error(request, message)
        return JsonResponse({'success': False, 'message': message})

    except Exception as e:
        message = f'An error occurred: {e}'
        messages.error(request, message)
        return JsonResponse({'success': False, 'message': message})


@login_required
def delete_notification(request, sku):
    user = request.user
    try:
        notification = Notification.objects.filter(sku=sku).first()

        if not notification:
            raise ObjectDoesNotExist('Notification does not exist')

        if (notification.user != user) and (not user.is_superuser):
            raise ValueError('You must be the owner of the notification to delete it.')

        notification.delete()

        message = 'Successfully deleted the notification!'
        messages.success(request, message)

        return JsonResponse({'success': True, 'message': message})

    except ObjectDoesNotExist as e:
        message = str(e)
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


@login_required
def delete_all_notifications(request, username):
    user = request.user
    try:
        user = request.user
        selected_user = User.objects.filter(username=username).first()

        if (selected_user != user) and (not user.is_superuser):
            raise ValueError('You must be the owner of these notifications to delete them.')

        notifications = Notification.objects.filter(user=user, cleared_status=True)

        notification_skus = []

        for notification in notifications:
            
            notification_skus.append(notification.sku)
            notification.delete()

        message = 'Successfully deleted the notifications!'
        messages.success(request, message)

        return JsonResponse({'success': True, 'message': message, 'skus': notification_skus})

    except Notification.DoesNotExist:
        message = 'Invalid Notification'
        messages.error(request, message)
        return JsonResponse({'success': False, 'message': message})

    except ValueError as e:
        message = f'Unsuccessfully deleted the notifications! - {e}'
        messages.error(request, message)
        return JsonResponse({'success': False, 'message': message})

    except Exception as e:
        message = f'An error occurred: {e}'
        messages.error(request, message)
        return JsonResponse({'success': False, 'message': message})
