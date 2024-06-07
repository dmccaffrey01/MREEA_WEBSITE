from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from .forms import TestimonialForm
from .models import Testimonial
from django.contrib import messages
from django.contrib.auth.models import User
from profiles.models import UserProfile
from .tasks import new_testimonial_approved_notification, new_testimonial_denied_notification, new_testimonial_notifications
from membership.models import Membership


def index(request):
    approved_testimonials = Testimonial.objects.filter(is_approved=True).order_by('?')

    random_testimonials = approved_testimonials[:5]

    for testimonial in random_testimonials:
        profile = UserProfile.objects.filter(user=testimonial.user).first()

        testimonial.profile = profile

    intro_profiles = random_testimonials[2:5]

    all_members = Membership.objects.all()

    members_count = all_members.count()

    rounded_members_count = (members_count // 5) * 5

    context = {
        'random_testimonials': random_testimonials,
        'intro_profiles': intro_profiles,
        'members_count': rounded_members_count,
    }

    return render(request, 'home/index.html', context)


def testimonials(request):

    approved_testimonials = Testimonial.objects.filter(is_approved=True, is_awaiting_approval=False).order_by('?')

    for testimonial in approved_testimonials:
        profile = UserProfile.objects.filter(user=testimonial.user).first()
        testimonial.profile = profile
    
    if request.user.is_superuser:
        awaiting_approval_testimonials = Testimonial.objects.filter(is_awaiting_approval=True)
        for testimonial in awaiting_approval_testimonials:
            profile = UserProfile.objects.filter(user=testimonial.user).first()
            testimonial.profile = profile
    else:
        awaiting_approval_testimonials = False

    testimonials_count = approved_testimonials.count()

    one_third = testimonials_count // 3

    remainder = testimonials_count % 3

    if remainder == 1:
        first_third = one_third + 1
        second_third = first_third + one_third
    elif remainder == 2:
        first_third = one_third + 1
        second_third = first_third + one_third + 1
    else:
        first_third = one_third
        second_third = first_third + one_third

    third_third = second_third + one_third

    containers = []

    for i in range(0, 3):
        if i == 0:
            container = approved_testimonials[:first_third]
            if remainder == 0:
                testimonial = 'half'
                container.append(testimonial)
        elif i == 1:
            container = approved_testimonials[second_third:third_third]
            if remainder == 0:
                testimonial = 'half'
                container.insert(0, testimonial)
            if remainder == 1 or remainder == 2:
                testimonial = 'half'
                container.insert(0, testimonial)
                container.append(testimonial)
        else:
            container = approved_testimonials[first_third:second_third]
            if remainder == 0:
                testimonial = 'half'
                container.append(testimonial)
            if remainder == 1:
                testimonial = 'full'
                container.append(testimonial)
        containers.append(container)

    context = {
        'testimonials_count': testimonials_count,
        'containers': containers,
        'awaiting_approval_testimonials': awaiting_approval_testimonials,
    }

    return render(request, 'testimonials/testimonials.html', context)
        

@login_required
def add_testimonial(request, username):

    user = request.user

    selected_user = User.objects.filter(username=username).first()

    if not selected_user:
        messages.error(request, "User does not exist!")
        return redirect(reverse('home'))

    if (user.username != username) and (not user.is_superuser):
        messages.error(request, "You can only add your own testimonial!")
        return redirect(reverse('home'))
    
    if request.method == 'POST':
        form = TestimonialForm(request.POST)

        if form.is_valid():
            form_data = form.cleaned_data

            testimonial_message = form_data['message']

            testimonial, created = Testimonial.objects.get_or_create(user=selected_user)

            testimonial.message = testimonial_message

            testimonial.save()

            # new_testimonial_notifications.delay(testimonial.id) # celery task

            messages.success(request, "Successfully added your testimonial! An admin will approve it shortly!")

            return redirect(reverse('testimonials'))

    else:
        form = TestimonialForm()

    action_url = reverse('add_testimonial', args=(username,))
    page_heading = 'Add Testimonial'

    testimonial = Testimonial.objects.filter(user=user).first()

    if testimonial:
        testimonial_message = testimonial.message
    else:
        testimonial_message = ''

    context = {
        'form': form,
        'action_url': action_url,
        'page_heading': page_heading,
        'testimonial_message': testimonial_message,
    }

    return render(request, 'testimonials/testimonial.html', context)


@login_required
def edit_testimonial(request, username):

    user = request.user

    selected_user = User.objects.filter(username=username).first()

    if not selected_user:
        messages.error(request, "User does not exist!")
        return redirect(reverse('home'))

    if (user.username != username) and (not user.is_superuser):
        messages.error(request, "You can only edit your own testimonial!")
        return redirect(reverse('home'))
    
    testimonial = Testimonial.objects.filter(user=selected_user).first()

    if not testimonial:
        messages.error(request, "Testimonial doesn't exist!")
        return redirect(reverse('home'))
    
    if request.method == 'POST':
        form = TestimonialForm(request.POST, instance=testimonial)

        if form.is_valid():
            form_data = form.cleaned_data

            testimonial_message = form_data['message']

            testimonial.message = testimonial_message

            testimonial.is_approved = False

            testimonial.is_awaiting_approval = True

            testimonial.save()

            # new_testimonial_notifications.delay(testimonial.id) # celery task

            messages.success(request, "Successfully edited your testimonial! An admin will approve it shortly!")

            return redirect(reverse('testimonials'))

    else:
        form = TestimonialForm(instance=testimonial)

    action_url = reverse('edit_testimonial', args=(username,))
    page_heading = 'Edit Testimonial'

    testimonial_message = testimonial.message

    selected_profile = UserProfile.objects.filter(user=selected_user).first()

    context = {
        'form': form,
        'action_url': action_url,
        'page_heading': page_heading,
        'testimonial_message': testimonial_message,
        'testimonial': testimonial,
        'selected_profile': selected_profile,
    }

    return render(request, 'testimonials/testimonial.html', context)


@login_required
def approve_testimonial(request, testimonial_id):

    user = request.user

    if not user.is_superuser:
        messages.error(request, "You must be an admin to approve this testimonial")
        return redirect(reverse('testimonials'))
    
    testimonial = Testimonial.objects.filter(id=testimonial_id).first()

    if not testimonial:
        messages.error(request, "Invalid testimonial")
        return redirect(reverse('testimonials'))
    
    testimonial.is_approved = True
    testimonial.is_awaiting_approval = False
    testimonial.save()

    # new_testimonial_approved_notification.delay(testimonial.id) # celery task

    messages.success(request, "Successfully approved testimonial")

    return redirect(reverse('testimonials'))


@login_required
def deny_testimonial(request, testimonial_id):

    user = request.user

    if not user.is_superuser:
        messages.error(request, "You must be an admin to deny this testimonial")
        return redirect(reverse('testimonials'))
    
    testimonial = Testimonial.objects.filter(id=testimonial_id).first()

    if not testimonial:
        messages.error(request, "Invalid testimonial")
        return redirect(reverse('testimonials'))
    
    testimonial.is_approved = False
    testimonial.is_awaiting_approval = False
    testimonial.save()

    # new_testimonial_denied_notification.delay(testimonial.id) # celery task

    messages.success(request, "Successfully denied testimonial")

    return redirect(reverse('testimonials'))


def privacy(request):

    return render(request, 'privacy/privacy.html')
