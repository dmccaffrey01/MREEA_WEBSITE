from django.shortcuts import reverse
from django.contrib.auth.models import User
from notifications.models import Notification
from .models import Testimonial
from profiles.models import UserProfile


def new_testimonial_notifications(testimonial_id):
    testimonial = Testimonial.objects.filter(id=testimonial_id).first()
    user_profile = UserProfile.objects.filter(user=testimonial.user).first()

    heading = f'New Testimonial - Awaiting Approval!'
    message = f'{user_profile.first_name} {user_profile.last_name} created a new testimonial and is awaiting approval.'
    category = 'testimonials'
    url = reverse('edit_testimonial', args=(testimonial.user.username,))

    admins = User.objects.filter(is_superuser=True)

    for admin in admins:
        new_notification = Notification.objects.create(
            user=admin,
            heading=heading,
            message=message,
            category=category,
            url=url,
        )
        new_notification.save()

    return "Successfully created notifications"


def new_testimonial_approved_notification(testimonial_id):
    testimonial = Testimonial.objects.filter(id=testimonial_id).first()

    heading = f'Testimonial Approved!'
    message = f'Your testimonial has been approved! \nIt will be visible on the homepage and testimonial wall.'
    category = 'testimonials'
    url = reverse('testimonials')

    new_notification = Notification.objects.create(
        user=testimonial.user,
        heading=heading,
        message=message,
        category=category,
        url=url,
    )
    new_notification.save()

    return "Successfully created notification"


def new_testimonial_denied_notification(testimonial_id):
    testimonial = Testimonial.objects.filter(id=testimonial_id).first()

    heading = f'Testimonial Denied'
    message = f'Your testimonial has been denied! \nPlease try again or contact us.'
    category = 'testimonials'
    url = reverse('edit_testimonial', args=(testimonial.user.username,))

    new_notification = Notification.objects.create(
        user=testimonial.user,
        heading=heading,
        message=message,
        category=category,
        url=url,
    )
    new_notification.save()

    return "Successfully created notification"
