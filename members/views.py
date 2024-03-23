from django.shortcuts import render, redirect, get_object_or_404, reverse
from profiles.models import UserProfile, Category, Class


def members(request):

    categories = Category.objects.all()
    category_and_classes = []
    for category in categories:
        category_and_classes.append({
            'category': category,
            'classes': Class.objects.filter(category=category)
        })

    if request.method == "POST":
        profiles = UserProfile.objects.all()

        first_name = request.POST.get('id_first_name')
        last_name = request.POST.get('id_last_name')
        classes = request.POST.get('id_classes')

        print(classes)

        if first_name:
            profiles = profiles.filter(first_name__icontains=first_name)
        if last_name:
            profiles = profiles.filter(last_name__icontains=last_name)

        context = {
            'search_query': True,
            'query_profiles': profiles,
            'category_and_classes': category_and_classes
        }

        return render(request, 'members/members.html', context)
        
    context = {
        'category_and_classes': category_and_classes,
    }

    return render(request, 'members/members.html', context)