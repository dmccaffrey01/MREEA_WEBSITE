from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from .forms import TestimonialForm
from .models import Testimonial
from django.contrib import messages
from django.contrib.auth.models import User
from profiles.models import UserProfile
from django.conf import settings


def index(request):
    approved_testimonials = Testimonial.objects.filter(is_approved=True).order_by('?')

    random_testimonials = approved_testimonials[:5]

    for testimonial in random_testimonials:
        profile = UserProfile.objects.filter(user=testimonial.user).first()

        testimonial.profile = profile

    context = {
        'random_testimonials': random_testimonials,
    }

    return render(request, 'home/index.html', context)


def testimonials(request):

    approved_testimonials = Testimonial.objects.filter(is_approved=True).order_by('?')

    testimonials_count = approved_testimonials.count()

    for testimonial in approved_testimonials:
        profile = UserProfile.objects.filter(user=testimonial.user).first()

        testimonial.profile = profile

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

            testimonial.save()

            messages.success(request, "Successfully edited your testimonial! An admin will approve it shortly!")

            return redirect(reverse('testimonials'))

    else:
        form = TestimonialForm(instance=testimonial)

    action_url = reverse('edit_testimonial', args=(username,))
    page_heading = 'Edit Testimonial'


    testimonial_message = testimonial.message

    context = {
        'form': form,
        'action_url': action_url,
        'page_heading': page_heading,
        'testimonial_message': testimonial_message,
    }

    return render(request, 'testimonials/testimonial.html', context)

