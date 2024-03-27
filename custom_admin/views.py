from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from profiles.models import UserProfile
from membership.models import Membership, MembershipStatus


@login_required
def admin(request):

    user = request.user

    if not user.is_superuser:
        return redirect(reverse('home'))

    context = {

    }

    return render(request, 'admin/admin.html', context)


@login_required
def user_admin(request):

    user = request.user

    if not user.is_superuser:
        return redirect(reverse('home'))
    
    all_users = User.objects.all()

    all_users_profiles_and_memberships = []

    for user in all_users:
        user_profile = UserProfile.objects.filter(user=user).first()
        membership = Membership.objects.filter(user=user).first()

        item = {
            'user': user,
            'profile': user_profile,
            'membership': membership,
        }

        all_users_profiles_and_memberships.append(item)

    all_users_profiles_and_memberships = sorted(
        all_users_profiles_and_memberships,
        key=lambda x: getattr(x['membership'], 'purchase_date', None),
        reverse=True
    )

    all_status_colors = set()

    all_memberships_statuses = Membership.objects.all()

    for membership in all_memberships_statuses:
        color = membership.status.color
        all_status_colors.add(color)

    # Convert the set to a comma-separated string
    color_string = ','.join(all_status_colors)

    context = {
        'all_users_profiles_and_memberships': all_users_profiles_and_memberships,
        'all_status_colors': color_string,
    }

    return render(request, 'admin/user_admin.html', context)