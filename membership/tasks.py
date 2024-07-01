from .models import Membership, MembershipStatus
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import reverse
from notifications.models import Notification
from django.contrib.auth.models import User
import os
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def check_memberships():
    today = timezone.now().date()

    memberships = Membership.objects.all().exclude(status__name='expired')

    expired_name = 'expired'
    expired_status = MembershipStatus.objects.filter(name=expired_name).first()
    expired_days_remaining = [30, 7, 1]
    expiring_members_list = []

    for membership in memberships:
        end_date = membership.end_date
        remaining_days = (end_date - today).days

        if end_date < today:
            membership.status = expired_status
            membership.status_name = expired_name
            membership.save()

            heading = f'Membership has expired'
            message = (f"Your membership expired on {end_date.strftime('%b %d %Y')}. "
                       f"If you want to renew your membership, go to the membership status page and click the renew button. "
                       f"If not, you won't be able to access membership material.")
            category = 'membership'
            url = reverse('membership_status')

            new_expiring_membership_notification(membership.user.username, heading, message, category, url)

        if remaining_days in expired_days_remaining:
            heading = f'Membership Expiring in {remaining_days} day(s)'
            message = (f"Your membership will expire on {end_date.strftime('%b %d %Y')}. "
                       f"If you want to renew your membership, go to the membership status page and click the renew button. "
                       f"If not, your membership will expire in {remaining_days} day(s).")
            category = 'membership'
            url = reverse('membership_status')

            new_expiring_membership_notification(membership.user.username, heading, message, category, url)

            expiring_members_list.append({
                'username': membership.user.username,
                'heading': heading,
                'message': message,
            })

    today = timezone.localtime(timezone.now())

    today = today.replace(hour=0, minute=5, second=0, microsecond=0)

    # if len(expiring_members_list):
    #     time_interval = timedelta(hours=2) / len(expiring_members_list)

    #     for i, item in enumerate(expiring_members_list):
    #         delay = today + i * time_interval
    #         send_new_expiring_membership_email.apply_async((item['username'], item['heading'], item['message']), eta=delay)

    return "Successfully checked memberships"


def new_expiring_membership_notification(username, heading, message, category, url):
    user = User.objects.filter(username=username).first()

    new_notification = Notification.objects.create(
        user=user,
        heading=heading,
        message=message,
        category=category,
        url=url,
    )

    new_notification.save()

    return "Successfully added expiring membership notification"


# def send_new_expiring_membership_email(username, heading, message):
#     user = User.objects.filter(username=username).first()
    
#     subject = f"MREEA - {heading}"

#     membership_status_url = os.environ.get('SITE_URL') + reverse('membership_status')

#     html_content = render_to_string('email/new_expiring_membership_email_template.html', {'user': user, 'message': message, 'membership_status_url': membership_status_url,})
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
