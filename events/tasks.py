from django.shortcuts import reverse
from django.contrib.auth.models import User
from notifications.models import Notification
from datetime import timedelta
from django.utils import timezone
from .models import Event
import os
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from membership.models import Membership


def new_event_notifications(event_name):
    all_members = Membership.objects.filter(status__valid=True)
    event = Event.objects.filter(name=event_name).first()

    heading = 'New Upcoming Event'
    message = f'{event.friendly_name}\n\n There was a new event posted on the events page. \nCheck it out!'
    category = 'events'
    url = reverse('events')

    for member in all_members:
        user = member.user
        new_notification = Notification.objects.create(
            user=user,
            heading=heading,
            message=message,
            category=category,
            url=url,
        )

        new_notification.save()

    return "Successfully created notifications and scheduled emails"


# @shared_task
# def send_new_event_email(event_name, username):
#     user = User.objects.filter(username=username).first()
#     event = Event.objects.filter(name=event_name).first()
    
#     subject = 'MREEA - New Upcoming Event'

#     events_url = os.environ.get('SITE_URL') + reverse('events')

#     html_content = render_to_string('email/new_event_email_template.html', {'user': user, 'event': event, 'events_url': events_url,})
#     message = strip_tags(html_content)
              
#     from_email = f"MREEA Website <{os.environ.get('HOST_EMAIL')}>"
#     to_email = [user.email]
#     reply_to = [from_email]

#     email = EmailMultiAlternatives(
#         subject,
#         message,
#         from_email,
#         to_email,
#         reply_to=reply_to,
#     )

#     email.attach_alternative(html_content, "text/html")
#     email.send()

#     return "Successfully sent new event email"
