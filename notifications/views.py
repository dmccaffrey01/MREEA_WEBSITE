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



@login_required
def delete_notification_from_view(request, sku):
    user = request.user
    try:
        notification = Notification.objects.filter(sku=sku).first()

        if not notification:
            raise ObjectDoesNotExist('Notification does not exist')

        if (notification.user != user) and (not user.is_superuser):
            raise ValueError('You must be the owner of the notification to delete it.')
        
        messages.success(request, "Successfully deleted the notification!")

        return redirect(reverse('home'))

    except ObjectDoesNotExist as e:
        message = str(e)
        messages.error(request, message)
        return redirect(reverse('home'))

    except ValueError as e:
        message = f'Unsuccessfully deleted the notification! - {e}'
        messages.error(request, message)
        return redirect(reverse('home'))

    except Exception as e:
        message = f'An error occurred: {e}'
        messages.error(request, message)
        return redirect(reverse('home'))


def get_messages(request):
    # Get messages from Django messages framework
    django_messages = messages.get_messages(request)

    if not django_messages:
        return JsonResponse({'messages': []})
    
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
