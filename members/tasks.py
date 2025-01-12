from django.shortcuts import reverse
from django.contrib.auth.models import User
from notifications.models import Notification


def new_membership_approved_notification(username):
    user = User.objects.filter(username=username).first()

    heading = f'Membership Approved!'
    message = f'Your membership is now active. You can now access the membership benefits!'
    category = 'membership'
    url = reverse('membership_status')

    new_notification = Notification.objects.create(
        user=user,
        heading=heading,
        message=message,
        category=category,
        url=url,
    )
    new_notification.save()

    return "Successfully created notification"

def new_membership_denied_notification(username):
    user = User.objects.filter(username=username).first()

    heading = f'Membership Denied!'
    message = f'Your membership payment was unsuccessful. Please try again or contact us!'
    category = 'membership'
    url = reverse('membership_status')

    new_notification = Notification.objects.create(
        user=user,
        heading=heading,
        message=message,
        category=category,
        url=url,
    )
    new_notification.save()

    return "Successfully created notification"
