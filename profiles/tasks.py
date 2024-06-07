from celery import shared_task
from django.shortcuts import reverse
from django.contrib.auth.models import User
from notifications.models import Notification


@shared_task
def new_password_change_notification(username):
    user = User.objects.filter(username=username).first()

    heading = f'Change Password!'
    message = f'Your password has not been changed. Please change your password from the default. \nClick the button below'
    category = 'password'
    url = reverse('account_change_password')

    new_notification = Notification.objects.create(
        user=user,
        heading=heading,
        message=message,
        category=category,
        url=url,
    )
    new_notification.save()

    return "Successfully created notification"