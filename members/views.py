from django.shortcuts import render, redirect, get_object_or_404, reverse
from profiles.models import UserProfile, Category, Class, TeachingState
from membership.models import Membership, MembershipStatus, MembershipPackage
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .tasks import new_membership_approved_notification, new_membership_denied_notification
from django.db.models import Count, Q
import csv
from django.http import HttpResponse
from datetime import datetime, timedelta


def members(request):

    active_memberships = Membership.objects.filter(status__valid=True)

    active_memberships = active_memberships.exclude(package__name="hidden_admin_membership")

    users_with_active_memberships = active_memberships.values_list('user', flat=True)

    profiles = UserProfile.objects.filter(user__in=users_with_active_memberships)

    profiles = profiles.order_by('?')

    first_name = ''
    last_name = ''

    categories = Category.objects.all()
    category_and_classes = []

    teaching_states = TeachingState.objects.all()

    if request.method == "POST":

        first_name = request.POST.get('id_first_name')
        last_name = request.POST.get('id_last_name')

        if first_name:
            profiles = profiles.filter(first_name__icontains=first_name)
        if last_name:
            profiles = profiles.filter(last_name__icontains=last_name)

        checked_classes = []
        checked_states = []

        for category in categories:
            classes_in_category = Class.objects.filter(category=category)

            for c in classes_in_category:
                class_name = c.name
                class_id = f'id_class_{class_name}'
                is_class_checked = request.POST.get(class_id)
                if is_class_checked:
                    c.is_checked = True
                    checked_classes.append(c)


            category_and_classes.append({
                'category': category,
                'classes': classes_in_category,
            })

        for state in teaching_states:
            state_code = state.code
            state_id = f'id_state_{state_code}'
            is_state_checked = request.POST.get(state_id)
            if is_state_checked:
                state.is_checked = True
                checked_states.append(state)
        
        profiles = filter_profile_classes(profiles, checked_classes)
        profiles = filter_profile_teaching_states(profiles, checked_states)

    else:
        for category in categories:
            classes_in_category = Class.objects.filter(category=category)

            for c in classes_in_category:
                c.is_checked = False

            category_and_classes.append({
                'category': category,
                'classes': classes_in_category,
            })

        for state in teaching_states:
            state.is_checked = False

    num_of_profiles = len(profiles)
        
    context = {
        'query_profiles': profiles,
        'num_of_profiles': num_of_profiles,
        'category_and_classes': category_and_classes,
        'teaching_states': teaching_states,
        'first_name': first_name,
        'last_name': last_name,
    }

    return render(request, 'members/members.html', context)


def filter_profile_classes(profiles, checked_classes):
    new_profiles = []
    for profile in profiles:
        has_all_classes = check_all_classes(profile, checked_classes)
        if has_all_classes:
            new_profiles.append(profile)

    return new_profiles


def check_all_classes(profile, checked_classes):

    profile_classes = profile.classes.all()

    for c in checked_classes:

        if not c in profile_classes:
            return False
        
    return True


def filter_profile_teaching_states(profiles, checked_teaching_states):
    new_profiles = []
    for profile in profiles:
        has_all_teaching_states = check_all_teaching_states(profile, checked_teaching_states)
        if has_all_teaching_states:
            new_profiles.append(profile)

    return new_profiles


def check_all_teaching_states(profile, checked_teaching_states):

    profile_teaching_states = profile.teaching_states.all()

    for c in checked_teaching_states:

        if not c in profile_teaching_states:
            return False
        
    return True


def get_member_classes(request, username):
    user_profile = UserProfile.objects.filter(user__username=username).first()
    categories = Category.objects.all()
    user_classes = user_profile.classes.all()
    
    category_and_classes = []
    for category in categories:
        category_classes = user_classes.filter(category=category)
        if category_classes:
            category_and_classes.append({
                'category_name': category.friendly_name,
                'classes': [cls.friendly_name for cls in category_classes],
            })

    return JsonResponse({'category_and_classes': category_and_classes})


@login_required
def members_management(request):

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

        if membership.status.name == 'pending' or membership.status.name == 'active_renewal_pending':
            item["pending_action"] = True
            all_users_profiles_and_memberships.insert(0, item)
        else:
            all_users_profiles_and_memberships.append(item)

    context = {
        'all_users_profiles_and_memberships': all_users_profiles_and_memberships,
    }

    return render(request, 'management/members_management.html', context)


@login_required
def change_admin_status(request, username):

    user = request.user

    if not user.is_superuser:
        messages.error(request, "You must be an admin to change admin status!")
        return redirect(reverse('home'))
    
    selected_user = User.objects.filter(username=username).first()

    if not selected_user:
        messages.error(request, "Invalid User!")
        return redirect(reverse('members_management'))
    
    if selected_user.is_superuser:
        selected_user.is_superuser = False
    else:
        selected_user.is_superuser = True

    selected_user.save()

    messages.success(request, 'Successfully updated admin status!')
    return redirect(reverse('members_management'))

@login_required
def change_membership_status(request, username, is_active):

    user = request.user

    if not user.is_superuser:
        messages.error(request, "You must be an admin to change membership status!")
        return redirect(reverse('home'))
    
    selected_user = User.objects.filter(username=username).first()

    if not selected_user:
        messages.error(request, "Invalid User!")
        return redirect(reverse('members_management'))
    
    membership = Membership.objects.filter(user=selected_user).first()

    if not membership:
        messages.error(request, "Invalid Membership!")
        return redirect(reverse('members_management'))
    
    if is_active == 'True':
        membership_status = MembershipStatus.objects.filter(name='active').first()
        membership.status = membership_status
        membership.make_active()
        new_membership_approved_notification(username)
    else:
        if membership.status.name == 'pending':
            membership_status = MembershipStatus.objects.filter(name='payment_unsuccessful').first()
        else:
            membership_status = MembershipStatus.objects.filter(name='active_renewal_unsuccessful').first()
        membership.status = membership_status
        membership.make_unsuccessful()
        new_membership_denied_notification(username)
    
    membership.save()

    messages.success(request, 'Successfully updated membership status!')
    return redirect(reverse('members_management'))
