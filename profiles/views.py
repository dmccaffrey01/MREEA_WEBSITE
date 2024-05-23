from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import EditProfileForm
from .models import UserProfile, Category, Class, ProfileLink, TeachingState
import unicodedata
from django.contrib.auth.models import User
from django.contrib import messages
from urllib.parse import urlparse
from django.contrib.auth.mixins import LoginRequiredMixin
from allauth.account.views import PasswordChangeView
from django.urls import reverse_lazy
import json


def profile(request, username):

    user = request.user

    if user.username == username or user.is_superuser:
        profile_editable = True
    else:
        profile_editable = False

    selected_user = get_object_or_404(User, username=username)
    
    user_profile = get_object_or_404(UserProfile, user=selected_user)

    categories = Category.objects.all()
    user_classes = user_profile.classes.all()
    category_and_classes = []
    if user_classes:
        for category in categories:
            category_and_classes.append({
                'category': category,
                'user_classes': user_classes.filter(category=category),
            })
    
    teaching_states = user_profile.teaching_states.all()

    if (not teaching_states) and (not category_and_classes):
        teaching_section = False
    else:
        teaching_section = True

    user_profile_links = user_profile.links.all()

    for link in user_profile_links:
        icon_data = get_link_icon_data(link.friendly_name)
        link.icon = icon_data['icon_html']
        link.icon_name = icon_data['icon_name']

    if (not user_profile_links) and (not user_profile.email) and not (user_profile.phone_number):
        info_section = False
    else:
        info_section = True

    context = {
        'profile_editable': profile_editable,
        'user_profile': user_profile,
        'category_and_classes': category_and_classes,
        'teaching_section': teaching_section,
        'info_section': info_section,
        'user_profile_links': user_profile_links,
        'teaching_states': teaching_states,
    }

    return render(request, 'profiles/profile.html', context)


def get_link_icon_data(friendly_name):
    split_name = friendly_name.split(".com")
    website = split_name[0]

    if website == 'facebook':
        icon_html = """
        <svg xmlns="http://www.w3.org/2000/svg" class="dark-text" viewBox="0 0 256 256">
            <path d="M128 24a104 104 0 1 0 104 104A104.11 104.11 0 0 0 128 24m8 191.63V152h24a8 8 0 0 0 0-16h-24v-24a16 16 0 0 1 16-16h16a8 8 0 0 0 0-16h-16a32 32 0 0 0-32 32v24H96a8 8 0 0 0 0 16h24v63.63a88 88 0 1 1 16 0" />
        </svg>
        """
        icon_name = 'Facebook'
    elif website == 'linkedin':
        icon_html = """
        <svg xmlns="http://www.w3.org/2000/svg" class="dark-text" viewBox="0 0 256 256">
            <path d="M216 24H40a16 16 0 0 0-16 16v176a16 16 0 0 0 16 16h176a16 16 0 0 0 16-16V40a16 16 0 0 0-16-16m0 192H40V40h176zM96 112v64a8 8 0 0 1-16 0v-64a8 8 0 0 1 16 0m88 28v36a8 8 0 0 1-16 0v-36a20 20 0 0 0-40 0v36a8 8 0 0 1-16 0v-64a8 8 0 0 1 15.79-1.78A36 36 0 0 1 184 140m-84-56a12 12 0 1 1-12-12a12 12 0 0 1 12 12" />
        </svg>
        """
        icon_name = 'LinkedIn'
    else:
        icon_html = """
        <svg xmlns="http://www.w3.org/2000/svg" class="dark-text" viewBox="0 0 256 256">
            <path d="M128 24a104 104 0 1 0 104 104A104.12 104.12 0 0 0 128 24m87.62 96h-39.83c-1.79-36.51-15.85-62.33-27.38-77.6a88.19 88.19 0 0 1 67.22 77.6ZM96.23 136h63.54c-2.31 41.61-22.23 67.11-31.77 77c-9.55-9.9-29.46-35.4-31.77-77m0-16c2.31-41.61 22.23-67.11 31.77-77c9.55 9.93 29.46 35.43 31.77 77Zm11.36-77.6C96.06 57.67 82 83.49 80.21 120H40.37a88.19 88.19 0 0 1 67.22-77.6M40.37 136h39.84c1.82 36.51 15.85 62.33 27.38 77.6A88.19 88.19 0 0 1 40.37 136m108 77.6c11.53-15.27 25.56-41.09 27.38-77.6h39.84a88.19 88.19 0 0 1-67.18 77.6Z" />
        </svg>
        """
        icon_name = 'Globe'
    
    icon_data = {
        'icon_html': icon_html,
        'icon_name': icon_name,
    }

    return icon_data


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
            
            arr_of_links = request.POST.get("id_arr_of_links", "[]")
            link_ids = json.loads(arr_of_links)
            links = []
            saved_links = []

            for id in link_ids:
                url = request.POST.get(f'{id}')
                friendly_name = get_url_friendly_name(url)
                id_split = id.split('_')
                id_num = id_split[len(id_split) -1 ]
                name = request.POST.get(f'id_pl_name_{id_num}')
                links.append({
                    'url': url,
                    'friendly_name': friendly_name,
                    'name': name,
                })

            for l in links:
                if l['name']:
                    saved_link = ProfileLink.objects.get(name=l['name'])
                    saved_link.friendly_name = l['friendly_name']
                    saved_link.url = l['url']
                else:
                    saved_link = ProfileLink.objects.create(user=selected_user, friendly_name=l['friendly_name'], url=l['url'])
                saved_link.save()
                saved_links.append(saved_link)

            for link in user_profile.links.all():
                if not (link in saved_links):
                    link.delete()

            for saved_link in saved_links:
                user_profile.links.add(saved_link)

            all_classes = Class.objects.all()

            for c in all_classes:
                is_class_selected = request.POST.get(f'id_class_{c.name}')
                if is_class_selected:
                    user_profile.classes.add(c)
                elif c in user_profile.classes.all():
                    user_profile.classes.remove(c)

            all_states = TeachingState.objects.all()

            for s in all_states:
                is_state_selected = request.POST.get(f'id_state_{s.code}')
                if is_state_selected:
                    user_profile.teaching_states.add(s)
                elif s in user_profile.teaching_states.all():
                    user_profile.teaching_states.remove(s)

            user_profile.first_name = form_data['first_name']
            user_profile.last_name = form_data['last_name']
            user_profile.bio = form_data['bio']
            user_profile.email = form_data['email']
            user_profile.phone_number = form_data['phone_number']

            user_profile.save()

            if user.username == username:
                message = 'Successfully saved your profile!'
            else:
                message = f"Successfully saved {username}'s profile!"
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

    user_states = user_profile.teaching_states.all()
    states_and_user_states = []
    teaching_states = TeachingState.objects.all()
    for state in teaching_states:
        if state in user_states:
            states_and_user_states.append({
                'state': state,
                'user_selected': True,
            })
        else:
            states_and_user_states.append({
                'state': state,
                'user_selected': False,
            })

    user_profile_links = user_profile.links.all()

    for link in user_profile_links:
        icon_data = get_link_icon_data(link.friendly_name)
        link.icon = icon_data['icon_html']
        link.icon_name = icon_data['icon_name']

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
        'user_profile_links': user_profile_links,
        'states_and_user_states': states_and_user_states,
    }

    return render(request, 'profiles/edit_profile.html', context)


def get_url_friendly_name(url):
    # Parse the URL
    parsed_url = urlparse(url)

    # Extract the netloc (domain) part
    netloc = parsed_url.netloc if parsed_url.netloc else parsed_url.path

    # Remove the 'www.' prefix if it exists
    if netloc.startswith("www."):
        netloc = netloc[4:]

    return netloc


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

        if user.username == username:
            message = 'Successfully Saved Your Profile Picture'
        else:
            message = f"Successfully Saved {username}'s Profile Picture"
        messages.success(request, message)

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


@login_required
def login_redirect(request):
    user = request.user

    user_profile = get_object_or_404(UserProfile, user=user)

    if not user_profile.is_password_changed:
        messages.warning(request, "Please change your password!")
        return redirect(reverse('account_change_password'))
    
    return redirect(reverse('profile', args=(user.username,)))


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy('login_redirect')

    
