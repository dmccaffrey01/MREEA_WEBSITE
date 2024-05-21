from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from profiles.models import UserProfile, Class
from membership.models import Membership, MembershipStatus, MembershipPackage
from django.http import JsonResponse
from django.contrib import messages


@login_required
def admin(request):

    user = request.user

    if not user.is_superuser:
        messages.error(request, "You must be an admin to continue!")
        return redirect(reverse('home'))
    
    context = {

    }

    return render(request, 'admin/admin.html', context)



@login_required
def user_admin(request):

    user = request.user

    if not user.is_superuser:
        messages.error(request, "You must be an admin to continue!")
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

        if membership.status.name == 'pending' or membership.status.name == 'active_pending':
            item["pending_action"] = True
            all_users_profiles_and_memberships.insert(0, item)
        else:
            all_users_profiles_and_memberships.append(item)

    context = {
        'all_users_profiles_and_memberships': all_users_profiles_and_memberships,
    }

    return render(request, 'user_management/user_admin.html', context)


@login_required
def change_membership_status(request, username, is_active):

    user = request.user

    if not user.is_superuser:
        messages.error(request, "You must be an admin to change membership status!")
        return redirect(reverse('home'))
    
    selected_user = User.objects.filter(username=username).first()

    if not selected_user:
        messages.error(request, "Invalid User!")
        return redirect(reverse('home'))
    
    membership = Membership.objects.filter(user=selected_user).first()

    if not membership:
        messages.error(request, "Invalid Membership!")
        return redirect(reverse('home'))
    
    if is_active == 'True':
        membership_status = MembershipStatus.objects.filter(name='active').first()
        membership.status = membership_status
        membership.make_active()
    else:
        if membership.status.name == 'pending':
            membership_status = MembershipStatus.objects.filter(name='payment_unsuccessful').first()
        else:
            membership_status = MembershipStatus.objects.filter(name='active_renewal_unsuccessful').first()
        membership.status = membership_status
        membership.make_unsuccessful()
    
    membership.save()

    messages.success(request, 'Successfully updated membership status!')
    return redirect(reverse('user_admin'))
    