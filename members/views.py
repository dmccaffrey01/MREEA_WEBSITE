from django.shortcuts import render, redirect, get_object_or_404, reverse
from profiles.models import UserProfile, Category, Class, TeachingState
from membership.models import Membership, MembershipStatus
from django.http import JsonResponse


def members(request):

    categories = Category.objects.all()
    category_and_classes = []

    teaching_states = TeachingState.objects.all()

    if request.method == "POST":

        active_memberships = Membership.objects.filter(status__valid=True)

        users_with_active_memberships = active_memberships.values_list('user', flat=True)

        profiles = UserProfile.objects.filter(user__in=users_with_active_memberships)

        first_name = request.POST.get('id_first_name')
        last_name = request.POST.get('id_last_name')

        if first_name:
            profiles = profiles.filter(first_name__icontains=first_name)
        if last_name:
            profiles = profiles.filter(last_name__icontains=last_name)

        for category in categories:
            classes_in_category = Class.objects.filter(category=category)

            for c in classes_in_category:
                class_name = c.name
                class_id = f'id_class_{class_name}'
                is_class_checked = request.POST.get(class_id)
                if is_class_checked:
                    c.is_checked = True
                    profiles = profiles.filter(classes__name=class_name)


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
                profiles = profiles.filter(teaching_states__code=state_code)

        profiles = profiles.order_by('?')

        context = {
            'query_profiles': profiles,
            'num_of_profiles': len(profiles),
            'category_and_classes': category_and_classes,
            'teaching_states': teaching_states,
            'first_name': first_name,
            'last_name': last_name,
        }

        return render(request, 'members/members_searched.html', context)
    
    for category in categories:
        category_and_classes.append({
            'category': category,
            'classes': Class.objects.filter(category=category)
        })
        
    context = {
        'category_and_classes': category_and_classes,
        'teaching_states': teaching_states,
    }

    return render(request, 'members/members.html', context)


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