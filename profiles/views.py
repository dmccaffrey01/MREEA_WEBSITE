from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import EditProfileForm
from .models import UserProfile, Category, Class
import unicodedata


def profile(request, username):

    user = request.user

    if user.username == username:
        profile_editable = True
    else:
        profile_editable = False

    user_profile = UserProfile.objects.filter(user__username=username).first()

    context = {
        'profile_editable': profile_editable,
        'user_profile': user_profile,
    }

    return render(request, 'profiles/profile.html', context)


@login_required
def edit_profile(request, username):

    user = request.user

    if user.username == username:
        profile_saveable = True
    else:
        profile_saveable = False
        return redirect(reverse('profile', args=(user.username)))
    
    user_profile = get_object_or_404(UserProfile, user=user)
    
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user_profile)

        if form.is_valid():
            form_data = form.cleaned_data
            category_name = form.cleaned_data['category_name']
            class_name = form.cleaned_data['class_name']

            category_field = Category.objects.get(name=category_name)
            class_field = Class.objects.get(name=class_name)

            user_profile.first_name = form_data["first_name"]
            user_profile.last_name = form_data["last_name"]
            user_profile.title = form_data["title"]
            user_profile.bio = form_data["bio"]
            user_profile.facebook_link = form_data["facebook_link"]
            user_profile.email = form_data["email"]
            user_profile.phone_number = form_data["phone_number"]
            user_profile.category_field = category_field
            user_profile.class_field = class_field

            user_profile.save()
            
            return redirect(reverse('profile', args=(user.username,)))
        
    else:
        form = EditProfileForm(instance=user_profile)

    all_categories = Category.objects.all()
    all_classes = Class.objects.all()
    normalized_text = unicodedata.normalize('NFC', user_profile.bio)
    bio_count = len(normalized_text)

    context = {
        'profile_saveable': profile_saveable,
        'form': form,
        'all_categories': all_categories,
        'all_classes': all_classes,
        'bio_count': bio_count,
    }

    return render(request, 'profiles/edit_profile.html', context)


@login_required
def edit_profile_picture(request, username):

    user = request.user

    if user.username == username:
        profile_saveable = True
    else:
        profile_saveable = False
        return redirect(reverse('profile', args=(user.username)))
    
    user_profile = get_object_or_404(UserProfile, user=user)
    
    if request.method == 'POST':
        if 'profile_picture' in request.FILES:
            profile_picture = request.FILES['profile_picture']
        else:
            return redirect(reverse('profile', args=(user.username,)))

        user_profile.image = profile_picture
        user_profile.save()

        return redirect(reverse('profile', args=(user.username,)))
            

    context = {
        'profile_saveable': profile_saveable,
    }

    return render(request, 'profiles/edit_profile_picture.html', context)
