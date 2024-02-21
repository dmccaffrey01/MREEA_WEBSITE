from django.shortcuts import render, redirect, get_object_or_404
from membership.models import Membership, MembershipStatus, MembershipUpdateStatus
from django.utils import timezone


def index(request):

    membership_update_status = MembershipUpdateStatus.objects.get(name="membership_update_status")

    today = timezone.now().date()

    if membership_update_status.last_updated_date < today:
        expired_membership_status = MembershipStatus.objects.get(name="expired")

        expired_memberships = Membership.objects.filter(end_date__lt=today).exclude(status=expired_membership_status)
        for membership in expired_memberships:
            membership.status = expired_membership_status
            membership.save()
        
        membership_update_status.last_updated_date = today
        membership_update_status.save()

    return render(request, 'home/index.html')