import os
import requests
from django.shortcuts import render, redirect, get_object_or_404
import json
from django.http import JsonResponse
from django.db.models import Q
from .forms import CustomSignupForm
from django.contrib.auth import login
from .models import Event, MemberProfile, ResourceLinkType, ResourceCategory, Resource, ResourceSubCategory, ImageSelect, AspectRatio
from .forms import EventForm, MemberProfileForm, ContactForm, MemberSearchForm, MemberProfilePictureForm, AddResourceForm
from django.core.mail import send_mail
from cloudinary.uploader import upload
import base64
from django.core.files.base import ContentFile
import cloudinary.uploader
from allauth.account.views import PasswordChangeView
from django.template.response import TemplateResponse
from django.conf import settings
from django.utils import timezone
from django.http import HttpResponseRedirect


def index(request):
    
    user = request.user

    if user.is_authenticated:
        member_profile = MemberProfile.objects.filter(user=user).first()
    else:
        member_profile = False

    context = {
        'member_profile': member_profile,
    }

    return render(request, 'index.html', context)


def membership(request):
    
    user = request.user

    if user.is_authenticated:
        member_profile = MemberProfile.objects.filter(user=user).first()
    else:
        member_profile = False

    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save(request)
            login(request, user)
            
            return redirect('membership')
    else:
        form = CustomSignupForm()
    

    logged_in = user.is_authenticated

    context = {
        'logged_in': logged_in,
        'member_profile': member_profile,
        'form': form,
    }

    return render(request, 'membership.html', context)



def signup_view(request):

    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save(request)
            login(request, user)
            
            return redirect('membership')
    else:
        form = CustomSignupForm()
    
    return render(request, 'account/signup.html', {
        'form': form,
    })


def announcements(request):
    
    user = request.user

    logged_in = user.is_authenticated

    is_admin = user.is_superuser

    if user.is_authenticated:
        member_profile = MemberProfile.objects.filter(user=user).first()
    else:
        member_profile = False

    events = Event.objects.all()

    current_date = timezone.now()

    upcoming_events = Event.objects.filter(end_date__gt=current_date).order_by('start_date')

    past_events = Event.objects.filter(end_date__lt=current_date).order_by('-end_date')

    context = {
        'logged_in': logged_in,
        'is_admin': is_admin,
        'events': events,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'member_profile': member_profile,
    }

    return render(request, 'announcements.html', context)


def edit_event(request, event_short_uuid):
    event = get_object_or_404(Event, event_short_uuid=event_short_uuid)

    event_resources = event.resources.all()

    number_of_event_resources = event_resources.count()

    resources = Resource.objects.filter(category__category="Event Resource").exclude(pk__in=event_resources)

    select_images = ImageSelect.objects.filter(Q(aspect_ratio__width=16) & Q(aspect_ratio__height=9))
    for image in select_images:
        print(image.name)

    if request.method == 'POST':
        if 'delete' in request.POST:
            event.delete()
            return redirect('announcements')
        
        event_form = EventForm(request.POST, instance=event)
        if event_form.is_valid():
            event = event_form.save()
            cropped_image_data = request.POST.get('croppedImageData')
            if cropped_image_data:
                # Decode the Base64 image data
                image_data = base64.b64decode(cropped_image_data.split(',')[-1])

                image_file = ContentFile(image_data)

                # Upload the image file to Cloudinary
                cloudinary_response = cloudinary.uploader.upload(image_file, public_id="event_image")

                # Save the Cloudinary image URL in the profile_image field of the MemberProfile model
                event.event_image = cloudinary_response['secure_url']
                event.save()

                aspect_ratio = AspectRatio.objects.get(width=16, height=9)

                image_name = event.title + ' Event'
                image_select = ImageSelect.objects.create(name=image_name, image=event.event_image, aspect_ratio=aspect_ratio)
                image_select.save()
            
            selected_resource_data = request.POST.get('selectedResources')
            if selected_resource_data:
                parsed_selected_resource_data = json.loads(selected_resource_data)

                for link in parsed_selected_resource_data:
                    resource = Resource.objects.get(link=link)
                    event.resources.add(resource)
                
                event.save()
            
            selected_image_data = request.POST.get('selectedImage')
            if selected_image_data:
                selected_image = ImageSelect.objects.get(image_uuid=selected_image_data)
                event.event_image = selected_image.image
                event.save()

            return redirect('announcements')
    else:
        event_form = EventForm(instance=event)
    
    context = {
        'event_form': event_form,
        'event': event,
        'edit_image': True,
        'resources': resources,
        'event_resources': event_resources,
        'number_of_event_resources': number_of_event_resources,
        'select_images': select_images,
    }
    return render(request, 'create_event.html', context)

def create_event(request):
    resources = Resource.objects.filter(category__category="Event Resource")

    select_images = ImageSelect.objects.filter(Q(aspect_ratio__width=16) & Q(aspect_ratio__height=9))
    
    if request.method == 'POST':
        event_form = EventForm(request.POST)
        if event_form.is_valid():
            event = event_form.save()

            cropped_image_data = request.POST.get('croppedImageData')
            if cropped_image_data:
                # Decode the Base64 image data
                image_data = base64.b64decode(cropped_image_data.split(',')[-1])

                image_file = ContentFile(image_data)

                # Upload the image file to Cloudinary
                cloudinary_response = cloudinary.uploader.upload(image_file, public_id="event_image")

                # Save the Cloudinary image URL in the profile_image field of the MemberProfile model
                event.event_image = cloudinary_response['secure_url']

                event.save()

                aspect_ratio = AspectRatio.objects.get(width=16, height=9)

                image_name = event.title + ' Event'
                image_select = ImageSelect.objects.create(name=image_name, image=event.event_image, aspect_ratio=aspect_ratio)
                image_select.save()
            
            selected_resource_data = request.POST.get('selectedResources')
            if selected_resource_data:
                parsed_selected_resource_data = json.loads(selected_resource_data)

                for link in parsed_selected_resource_data:
                    resource = Resource.objects.get(link=link)
                    event.resources.add(resource)
                
                event.save()
            
            selected_image_data = request.POST.get('selectedImage')
            if selected_image_data:
                selected_image = ImageSelect.objects.get(image_uuid=selected_image_data)
                event.event_image = selected_image.image
                event.save()

            return redirect('announcements')
    else:
        event_form = EventForm()
    
    context = {
        'event_form': event_form,
        'edit_image': True,
        'resources': resources,
        'event_resources': False,
        'number_of_event_resources': 0,
        'select_images': select_images,
    }
    return render(request, 'create_event.html', context)


def event_detail(request, event_short_uuid):
    event = Event.objects.get(event_short_uuid=event_short_uuid)

    event_resources = event.resources.all()
    
    context = {
        'event': event,
        'event_resources': event_resources
    }

    return render(request, 'event_detail.html', context)


def get_event_data(request):
    events = Event.objects.all()

    events_values = events.values()

    data = {
        'events': list(events_values),
    }

    return JsonResponse(data, safe=False)


def members(request):

    user = request.user

    if user.is_authenticated:
        member_profile = MemberProfile.objects.filter(user=user).first()
    else:
        member_profile = False

    form = MemberSearchForm()
    members = None
    search_results = False

    if request.method == 'GET':
        form = MemberSearchForm(request.GET)
        if form.is_valid():
            last_name = form.cleaned_data.get('last_name')
            first_name = form.cleaned_data.get('first_name')
            teaching_category = form.cleaned_data.get('teaching_category')
            classes = form.cleaned_data.get('classes')

            # Query the MemberProfile model based on the search criteria
            members = MemberProfile.objects.all()

            # Apply filters based on search criteria if provided
            if last_name:
                members = members.filter(last_name__icontains=last_name)
            if first_name:
                members = members.filter(first_name__icontains=first_name)
            if teaching_category:
                members = members.filter(teaching_category__icontains=teaching_category)
            if classes:
                members = members.filter(classes__icontains=classes)
            search_results = True

    context = {
        'members': members,
        'form': form,
        'search_results': search_results,
        'member_profile': member_profile,
    }

    # Render the members.html template with the context
    return render(request, 'members.html', context)


def member_profile(request, member_short_uuid):
    user = request.user

    member_profile, created = MemberProfile.objects.get_or_create(user=user)

    member_profile.save()

    context = {
        'user': user,
        'member_profile': member_profile,
    }

    return render(request, 'member-profile.html', context)


def edit_member_profile(request, member_short_uuid):
    user = request.user
    
    member_profile = get_object_or_404(MemberProfile, user__member_short_uuid=member_short_uuid)

    if request.method == 'POST':
        if 'cancel' in request.POST:
            return redirect('member_profile', member_short_uuid=member_short_uuid)
        form = MemberProfileForm(request.POST, instance=member_profile)
        if form.is_valid():
            form.save()
            return redirect('member_profile', member_short_uuid=member_short_uuid)
    else:
        form = MemberProfileForm(instance=member_profile)
    
    context = {
        'user': user,
        'form': form,
        'member_profile': member_profile,
        'edit_profile': True,
    }

    return render(request, 'member-profile.html', context)


def edit_profile_picture(request, member_short_uuid):
    user = request.user

    member_profile = get_object_or_404(MemberProfile, user__member_short_uuid=member_short_uuid)

    if request.method == 'POST':
        if 'cancel' in request.POST:
            return redirect('member_profile', member_short_uuid=member_short_uuid)
        form = MemberProfilePictureForm(request.POST, instance=member_profile)
        if form.is_valid():
            form.save()
            cropped_image_data = request.POST.get('croppedImageData')
        if cropped_image_data:
            # Decode the Base64 image data
            image_data = base64.b64decode(cropped_image_data.split(',')[-1])

            image_file = ContentFile(image_data)

            # Upload the image file to Cloudinary
            cloudinary_response = cloudinary.uploader.upload(image_file, public_id="profile_image")

            # Save the Cloudinary image URL in the profile_image field of the MemberProfile model
            member_profile = MemberProfile.objects.get(user=request.user)
            member_profile.profile_image = cloudinary_response['secure_url']
            member_profile.save()
            return redirect('member_profile', member_short_uuid=member_short_uuid)
    else:
        form = MemberProfilePictureForm(instance=member_profile)

    context = {
        'user': user,
        'form': form,
        'member_profile': member_profile,
        'edit_profile': True,
        'edit_image': True,
    }

    return render(request, 'member-profile.html', context)


def learn_page(request):
    user = request.user

    if user.is_authenticated:
        member_profile = MemberProfile.objects.filter(user=user).first()
    else:
        member_profile = False

    context = {
        'user': user,
        'member_profile': member_profile,
    }

    return render(request, 'learn.html', context)


def contact_page(request):
    user = request.user

    if user.is_authenticated:
        member_profile = MemberProfile.objects.filter(user=user).first()
    else:
        member_profile = False

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            send_contact_email(form.cleaned_data)  # Send the email
            return redirect('announcements')
    else:
        form = ContactForm()

    context = {
        'user': user,
        'form': form,
        'member_profile': member_profile,
    }

    return render(request, 'contact.html', context)


def send_contact_email(data):
    subject = 'New Contact Message'
    message = f"Name: {data['name']}\nEmail: {data['email']}\n\n{data['message']}"
    from_email = os.environ.get('HOST_EMAIL')  # Update with your email address
    to_email = [os.environ.get('CONTACT_TO_EMAIL')]  # Update with the recipient's email address
    send_mail(subject, message, from_email, to_email)


class CustomPasswordChangeView(PasswordChangeView):
    def form_valid(self, form):
        response = super().form_valid(form)
        success_message = "Your password has been successfully changed."
        return TemplateResponse(self.request, settings.POPUP_MESSAGE_TEMPLATE, {'message': success_message})
    

def resources_page(request):
    user = request.user

    if user.is_authenticated:
        member_profile = MemberProfile.objects.filter(user=user).first()
    else:
        member_profile = None
    
    # create_subcategory(request)

    # Query all categories and subcategories
    categories = ResourceCategory.objects.all()
    subcategories = ResourceSubCategory.objects.all()

    # Create a dictionary to store category, subcategory, and their associated resources
    categories_with_subcategories = {}
    for category in categories:
        subcategories_for_category = subcategories.filter(category=category)
        subcategories_with_resources = {}
        for subcategory in subcategories_for_category:
            resources = Resource.objects.filter(subcategory=subcategory)
            subcategories_with_resources[subcategory] = resources
        categories_with_subcategories[category] = subcategories_with_resources
        
    context = {
        'user': user,
        'member_profile': member_profile,
        'categories_with_subcategories': categories_with_subcategories,
    }

    return render(request, 'resources.html', context)


def add_resource(request):
    user = request.user

    if user.is_authenticated:
        member_profile = MemberProfile.objects.filter(user=user).first()
    else:
        member_profile = False

    if request.method == 'POST':
        add_resource_form = AddResourceForm(request.POST)
        if add_resource_form.is_valid():
            new_resource = add_resource_form.save(commit=False)
            selected_category = request.POST.get('id_category_input')
            selected_subcategory = request.POST.get('id_subcategory_input')
            selected_link_type = request.POST.get('id_link_type_input')

            link_type = ResourceLinkType.objects.filter(link_type=selected_link_type).first()
            category = ResourceCategory.objects.filter(category=selected_category).first()
            subcategory = ResourceSubCategory.objects.filter(subcategory=selected_subcategory, category=category).first()

            new_resource.link_type = link_type
            new_resource.category = category
            new_resource.subcategory = subcategory

            new_resource.save()
            
            return redirect('resources')
    else:
        add_resource_form = AddResourceForm()

    link_types = ResourceLinkType.objects.all()
    categories = ResourceCategory.objects.all()
    subcategories = ResourceSubCategory.objects.all()
    
    context = {
        'user': user,
        'member_profile': member_profile,
        'add_resource_form': add_resource_form,
        'link_types': link_types,
        'categories': categories,
        'subcategories': subcategories,
    }

    return render(request, 'add-resource.html', context)


def create_subcategory(request):
    categories = ResourceCategory.objects.all()

    for category in categories:
        subcategory, created = ResourceSubCategory.objects.get_or_create(category=category)
        subcategory.save()