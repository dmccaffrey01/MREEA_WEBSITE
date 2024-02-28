from django.shortcuts import render, redirect, get_object_or_404, reverse
from .forms import MembersSearchForm
from profiles.models import UserProfile, Category, Class


def members(request):
    if request.method == "POST":
        form = MembersSearchForm(request.POST)
        profiles = UserProfile.objects.all()

        if form.is_valid():
            form_data = form.cleaned_data
            first_name = form_data.get('first_name')
            last_name = form_data.get('last_name')
            category_name = form_data.get('category_name')
            class_name = form_data.get('class_name')

            if first_name:
                profiles = profiles.filter(first_name__icontains=first_name)
            if last_name:
                profiles = profiles.filter(last_name__icontains=last_name)
            if category_name:
                profiles = profiles.filter(category_field__name=category_name)
            if class_name:
                profiles = profiles.filter(class_field__name=class_name)

            context = {
                'search_query': True,
                'query_profiles': profiles,
                'form': form,
            }
            return render(request, 'members/members.html', context)
    else:
        form = MembersSearchForm()

    context = {
        'form': form,
    }

    return render(request, 'members/members.html', context)