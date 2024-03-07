from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required


@login_required
def member_management(request):

    user = request.user

    if not user.is_superuser:
        return redirect(reverse('home'))

    context = {

    }

    return render(request, 'profiles/profile.html', context)