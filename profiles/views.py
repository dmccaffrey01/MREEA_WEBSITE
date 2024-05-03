from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import EditProfileForm
from .models import UserProfile, Category, Class, ProfileLink
import unicodedata
from django.contrib.auth.models import User
from django.contrib import messages


def profile(request, username):

    user = request.user

    if user.username == username or user.is_superuser:
        profile_editable = True
    else:
        profile_editable = False

    user_profile = UserProfile.objects.filter(user__username=username).first()

    categories = Category.objects.all()
    user_classes = user_profile.classes.all()
    category_and_classes = []
    for category in categories:
        category_and_classes.append({
            'category': category,
            'user_classes': user_classes.filter(category=category),
        })

    context = {
        'profile_editable': profile_editable,
        'user_profile': user_profile,
        'category_and_classes': category_and_classes,
    }

    if user.username == username:
        message = 'Viewing Your Profile'
    else:
        message = f"Viewing {username}'s Profile"
    messages.info(request, message)

    return render(request, 'profiles/profile.html', context)


@login_required
def edit_profile(request, username):

    user = request.user

    if user.username == username or user.is_superuser:
        profile_saveable = True
    else:
        profile_saveable = False
        return redirect(reverse('profile', args=(user.username,)))
    
    selected_user = get_object_or_404(User, username=username)
    
    user_profile = get_object_or_404(UserProfile, user=selected_user)
    
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user_profile)

        if form.is_valid():
            form_data = form.cleaned_data
            
            num_of_links_str = request.POST.get("id_num_of_links")
            num_of_links = int(num_of_links_str)

            links = []
            saved_links = []

            for i in range(1, num_of_links + 1):
                link = request.POST.get(f'id_pl_link_{i}')
                friendly_name = request.POST.get(f'id_pl_friendly_name_{i}')
                name = request.POST.get(f'id_pl_name_{i}')
                links.append({
                    'link': link,
                    'friendly_name': friendly_name,
                    'name': name,
                })

            for l in links:
                if l['name']:
                    saved_link = ProfileLink.objects.get(name=l['name'])
                    saved_link.friendly_name = l['friendly_name']
                    saved_link.link = l['link']
                else:
                    saved_link = ProfileLink.objects.create(user=user, friendly_name=l['friendly_name'], link=l['link'])
                saved_link.save()
                saved_links.append(saved_link)

            for saved_link in saved_links:
                user_profile.links.add(saved_link)

            all_classes = Class.objects.all()

            for c in all_classes:
                is_class_selected = request.POST.get(f'id_class_{c.name}')
                if is_class_selected:
                    user_profile.classes.add(c)
                elif c in user_profile.classes.all():
                    user_profile.classes.remove(c)

            user_profile.first_name = form_data['first_name']
            user_profile.last_name = form_data['last_name']
            user_profile.title = form_data['title']
            user_profile.bio = form_data['bio']
            user_profile.email = form_data['email']
            user_profile.phone_number = form_data['phone_number']

            user_profile.save()

            if user.username == username:
                message = 'Saved Your Profile'
            else:
                message = f"Saved {username}'s Profile"
            messages.success(request, message)
            
            return redirect(reverse('profile', args=(user.username,)))
        
    else:
        form = EditProfileForm(instance=user_profile)

    
    categories = Category.objects.all()
    user_classes = user_profile.classes.all()
    classes_and_user_classes = []
    classes = Class.objects.all()
    for item in classes:
        if item in user_classes:
            classes_and_user_classes.append({
                'item': item,
                'user_selected': True,
            })
        else:
            classes_and_user_classes.append({
                'item': item,
                'user_selected': False,
            })

    category_and_classes = []
    for category in categories:
        filtered_classes = [c for c in classes_and_user_classes if c['item'].category == category]
        category_and_classes.append({
            'category': category,
            'classes': filtered_classes,
        })

    normalized_text = unicodedata.normalize('NFC', user_profile.bio)
    bio_count = len(normalized_text)

    if user.username == username:
        message = 'Editing Your Profile'
    else:
        message = f"Editing {username}'s Profile"
    messages.info(request, message)

    context = {
        'profile_saveable': profile_saveable,
        'form': form,
        'bio_count': bio_count,
        'user_profile': user_profile,
        'category_and_classes': category_and_classes,
    }

    return render(request, 'profiles/edit_profile.html', context)


@login_required
def edit_profile_picture(request, username):

    user = request.user

    if user.username == username or user.is_superuser:
        profile_saveable = True
    else:
        profile_saveable = False
        return redirect(reverse('profile', args=(user.username,)))
    
    user_profile = get_object_or_404(UserProfile, user=user)
    
    if request.method == 'POST':
        if 'profile_picture' in request.FILES:
            profile_picture = request.FILES['profile_picture']
        else:
            return redirect(reverse('profile', args=(user.username,)))

        user_profile.image = profile_picture
        user_profile.save()

        return redirect(reverse('profile', args=(user.username,)))
            
    if user.username == username:
        message = 'Editing Your Profile Picture'
    else:
        message = f"Editing {username}'s Profile Picture"
    messages.info(request, message)

    context = {
        'profile_saveable': profile_saveable,
        'user_profile': user_profile,
    }

    return render(request, 'profiles/edit_profile_picture.html', context)
