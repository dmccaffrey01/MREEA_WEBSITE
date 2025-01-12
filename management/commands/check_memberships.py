from django.core.management.base import BaseCommand
from django.utils import timezone
from membership.models import Membership, MembershipStatus
from notifications.models import Notification
from django.contrib.auth.models import User
from django.urls import reverse

class Command(BaseCommand):
    help = 'Check memberships and update statuses and notifications'

    def handle(self, *args, **kwargs):
        self.check_memberships()

    def check_memberships(self):
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

                self.new_expiring_membership_notification(membership.user.username, heading, message, category, url)

            if remaining_days in expired_days_remaining:
                heading = f'Membership Expiring in {remaining_days} day(s)'
                message = (f"Your membership will expire on {end_date.strftime('%b %d %Y')}. "
                           f"If you want to renew your membership, go to the membership status page and click the renew button. "
                           f"If not, your membership will expire in {remaining_days} day(s).")
                category = 'membership'
                url = reverse('membership_status')

                self.new_expiring_membership_notification(membership.user.username, heading, message, category, url)

                expiring_members_list.append({
                    'username': membership.user.username,
                    'heading': heading,
                    'message': message,
                })

        today = timezone.localtime(timezone.now())
        today = today.replace(hour=0, minute=5, second=0, microsecond=0)

        return "Successfully checked memberships"

    def new_expiring_membership_notification(self, username, heading, message, category, url):
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
