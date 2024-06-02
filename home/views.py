from django.shortcuts import render, redirect, get_object_or_404
from membership.models import Membership, MembershipStatus
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import TestimonialForm
from .models import Testimonial


def index(request):

    return render(request, 'home/index.html')


def testimonials(request):

    return render(request, 'testimonials/testimonials.html')


@login_required
def add_testimonial(request):

    user = request.user

    form = TestimonialForm()

    context = {
        'form': form,
    }

    return render(request, 'home/index.html', context)


