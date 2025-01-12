from django.shortcuts import reverse
from django.contrib.auth.models import User
from notifications.models import Notification
from datetime import timedelta
from django.utils import timezone
from .models import Announcement
import os
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from membership.models import Membership


def new_announcement_notifications(announcement_name):
    all_members = Membership.objects.filter(status__valid=True)
    announcement = Announcement.objects.filter(name=announcement_name).first()

    heading = 'New Announcement'
    message = f'{announcement.friendly_name}\n\n There was a new announcement posted on the announcements page. \nCheck it out!'
    category = 'announcements'
    url = reverse('announcements')

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

    # tomorrow = timezone.localtime(timezone.now() + timedelta(days=1))
    # tomorrow_8_am = tomorrow.replace(hour=8, minute=0, second=0, microsecond=0)

    # time_interval = timedelta(hours=12) / all_members.count()

    # for i, member in enumerate(all_members):
    #     delay = tomorrow_8_am + i * time_interval
    #     username = member.user.username
    #     send_new_announcement_email.apply_async((announcement_name, username), eta=delay)

    return "Successfully created notifications and scheduled emails"


# def send_new_announcement_email(announcement_name, username):
#     user = User.objects.filter(username=username).first()
#     announcement = Announcement.objects.filter(name=announcement_name).first()
    
#     subject = 'MREEA - New Upcoming Announcement'

#     announcements_url = os.environ.get('SITE_URL') + reverse('announcements')

#     html_content = render_to_string('email/new_announcement_email_template.html', {'user': user, 'announcement': announcement, 'announcements_url': announcements_url,})
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

#     return "Successfully sent new announcement email"
