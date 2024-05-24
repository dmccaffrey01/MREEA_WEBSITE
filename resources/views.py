from django.shortcuts import render, redirect, reverse
from .models import Resource, Folder, Icon
from django.contrib.auth.decorators import login_required
from membership.models import Membership
from django.contrib import messages
from .forms import ManageResourceForm, ManageFolderForm
from profiles.views import get_url_friendly_name


@login_required
def resources(request):

    user = request.user

    membership = Membership.objects.get(user=user)

    if membership:
        if not membership.status.valid:
            messages.error("You must have a valid membership to access this!")
            return redirect(reverse('membership'))
    else:
        messages.error("You must have a valid membership to access this!")
        return redirect(reverse('membership'))
    
    return redirect(reverse('folder', args=('all',)))


@login_required
def folder(request, folder_name):

    user = request.user

    membership = Membership.objects.get(user=user)

    if membership:
        if not membership.status.valid:
            messages.error("You must have a valid membership to access this!")
            return redirect(reverse('membership'))
    else:
        messages.error("You must have a valid membership to access this!")
        return redirect(reverse('membership'))
    
    folder = Folder.objects.filter(name=folder_name).first()

    sub_folders = Folder.objects.filter(parent_folder=folder).order_by('-created_at')

    resources = Resource.objects.filter(folder=folder).order_by('-created_at')

    parent_folders = get_parent_folders(folder)

    parent_folders.reverse()

    if not (sub_folders or resources):
        no_resources_or_folders = True
    else:
        no_resources_or_folders = False

    context = {
        'folder': folder,
        'sub_folders': sub_folders,
        'resources': resources,
        'parent_folders': parent_folders,
        'no_resources_or_folders': no_resources_or_folders,
    }

    return render(request, 'resources/resources.html', context)


def get_parent_folders(folder, arr=None):
    if arr is None:
        arr = []
        
    new_arr = list(arr)
    
    new_arr.append(folder)

    if not folder.parent_folder:
        return new_arr
    else:
        parent_folder = folder.parent_folder
        if parent_folder:
            return get_parent_folders(parent_folder, new_arr)
        else:
            return new_arr
        

def get_icon_from_url(url):
    url_name = url.split('.com')[0]

    if url_name == 'drive.google':
        icon = Icon.objects.filter(name='google_drive').first()
    else:
        icon = Icon.objects.filter(name=url_name).first()
    
    if not icon:
        icon = Icon.objects.filter(name='resource').first()
    
    return icon


@login_required
def add_resource(request, folder_name):

    user = request.user

    if not user.is_superuser:
        messages.error(request, "You must be an admin to add a resource!")
        return redirect(reverse('home'))
    
    folder = Folder.objects.filter(name=folder_name).first()

    if folder:
        redirect_url = reverse('folder', args=(folder.name,))
    else:
        redirect_url = reverse('resources')
    
    if request.method == 'POST':
        form = ManageResourceForm(request.POST)

        if form.is_valid():
            form_data = form.cleaned_data
            resource_friendly_name = form_data['friendly_name']
            resource_url = form_data['url']

            url_friendly_name = get_url_friendly_name(resource_url)

            resource_icon = get_icon_from_url(url_friendly_name)

            new_resource = Resource.objects.create(
                friendly_name=resource_friendly_name,
                folder=folder,
                url=resource_url,
                icon=resource_icon,
            )

            new_resource.save()

            messages.success(request, "Successfully created resource!")

            return redirect(redirect_url)
    else:
        form = ManageResourceForm()

    management_name = 'Add Resource'

    management_icon = Icon.objects.filter(name='resource').first()

    action_url = reverse('add_resource', args=(folder.name,))

    sub_folders = Folder.objects.filter(parent_folder=folder).order_by('-created_at')

    resources = Resource.objects.filter(folder=folder).order_by('-created_at')

    parent_folders = get_parent_folders(folder)

    parent_folders.reverse()

    if not (sub_folders or resources):
        no_resources_or_folders = True
    else:
        no_resources_or_folders = False

    context = {
        'form': form,
        'folder': folder,
        'sub_folders': sub_folders,
        'resources': resources,
        'parent_folders': parent_folders,
        'no_resources_or_folders': no_resources_or_folders,
        'management_name': management_name,
        'management_icon': management_icon,
        'action_url': action_url,
    }

    return render(request, 'resources/resource_management.html', context)


@login_required
def edit_resource(request, folder_name, resource_name):

    user = request.user

    if not user.is_superuser:
        messages.error(request, "You must be an admin to edit a resource!")
        return redirect(reverse('home'))
    
    folder = Folder.objects.filter(name=folder_name).first()

    if folder:
        redirect_url = reverse('folder', args=(folder.name,))
    else:
        redirect_url = reverse('resources')

    resource = Resource.objects.filter(name=resource_name).first()

    if not resource:
        messages.error(request, "Invalid resource!")
        return redirect(redirect_url)    
    
    if request.method == 'POST':
        form = ManageResourceForm(request.POST)

        if form.is_valid():
            form_data = form.cleaned_data
            resource_friendly_name = form_data['friendly_name']
            resource_url = form_data['url']

            url_friendly_name = get_url_friendly_name(resource_url)

            resource_icon = get_icon_from_url(url_friendly_name)

            resource.friendly_name = resource_friendly_name
            resource.url = resource_url
            resource.icon = resource_icon
            resource.save()

            messages.success(request, "Successfully edited resource!")

            return redirect(redirect_url)
    else:
        form = ManageResourceForm(instance=resource)

    management_name = 'Edit Resource'

    management_icon = Icon.objects.filter(name='resource').first()

    action_url = reverse('edit_resource', args=(folder.name, resource.name,))

    sub_folders = Folder.objects.filter(parent_folder=folder).order_by('-created_at')

    resources = Resource.objects.filter(folder=folder).order_by('-created_at')

    parent_folders = get_parent_folders(folder)

    parent_folders.reverse()

    if not (sub_folders or resources):
        no_resources_or_folders = True
    else:
        no_resources_or_folders = False

    context = {
        'form': form,
        'folder': folder,
        'resource': resource,
        'sub_folders': sub_folders,
        'resources': resources,
        'parent_folders': parent_folders,
        'no_resources_or_folders': no_resources_or_folders,
        'management_name': management_name,
        'management_icon': management_icon,
        'action_url': action_url,
        'delete_btn': True,
    }

    return render(request, 'resources/resource_management.html', context)


@login_required
def delete_resource(request, folder_name, resource_name):

    user = request.user

    if not user.is_superuser:
        messages.error(request, "You must be an admin to delete a resource!")
        return redirect(reverse('home'))
    
    folder = Folder.objects.filter(name=folder_name).first()

    if folder:
        redirect_url = reverse('folder', args=(folder.name,))
    else:
        redirect_url = reverse('resources')

    resource = Resource.objects.filter(name=resource_name).first()

    if not resource:
        messages.error(request, "Invalid resource!")
        return redirect(redirect_url)
    
    resource.delete()

    messages.success(request, "Successfully deleted resource!")
    return redirect(redirect_url)

@login_required
def add_folder(request, folder_name):

    user = request.user

    if not user.is_superuser:
        messages.error(request, "You must be an admin to add a folder!")
        return redirect(reverse('home'))
    
    folder = Folder.objects.filter(name=folder_name).first()

    if folder:
        redirect_url = reverse('folder', args=(folder.name,))
    else:
        redirect_url = reverse('resources')
    
    if request.method == 'POST':
        form = ManageFolderForm(request.POST)

        if form.is_valid():
            form_data = form.cleaned_data
            folder_friendly_name = form_data['friendly_name']

            folder_icon = Icon.objects.filter(name='folder').first()

            new_folder = Folder.objects.create(
                friendly_name=folder_friendly_name,
                parent_folder=folder,
                icon=folder_icon,
            )

            new_folder.save()

            messages.success(request, "Successfully created folder!")

            return redirect(redirect_url)
    else:
        form = ManageFolderForm()

    management_name = 'Add Folder'

    management_icon = Icon.objects.filter(name='folder').first()

    action_url = reverse('add_folder', args=(folder.name,))

    sub_folders = Folder.objects.filter(parent_folder=folder).order_by('-created_at')

    resources = Resource.objects.filter(folder=folder).order_by('-created_at')

    parent_folders = get_parent_folders(folder)

    parent_folders.reverse()

    if not (sub_folders or resources):
        no_resources_or_folders = True
    else:
        no_resources_or_folders = False

    context = {
        'form': form,
        'folder': folder,
        'sub_folders': sub_folders,
        'resources': resources,
        'parent_folders': parent_folders,
        'no_resources_or_folders': no_resources_or_folders,
        'management_name': management_name,
        'management_icon': management_icon,
        'action_url': action_url,
    }

    return render(request, 'resources/folder_management.html', context)


@login_required
def edit_folder(request, folder_name, selected_folder_name):

    user = request.user

    if not user.is_superuser:
        messages.error(request, "You must be an admin to edit a resource!")
        return redirect(reverse('home'))
    
    folder = Folder.objects.filter(name=folder_name).first()

    if folder:
        redirect_url = reverse('folder', args=(folder.name,))
    else:
        redirect_url = reverse('resources')

    selected_folder = Folder.objects.filter(name=selected_folder_name).first()

    if not selected_folder:
        messages.error(request, "Invalid folder!")
        return redirect(redirect_url)    
    
    if request.method == 'POST':
        form = ManageFolderForm(request.POST)

        if form.is_valid():
            form_data = form.cleaned_data
            folder_friendly_name = form_data['friendly_name']

            selected_folder.friendly_name = folder_friendly_name
            selected_folder.save()

            messages.success(request, "Successfully edited folder!")

            return redirect(redirect_url)
    else:
        form = ManageFolderForm(instance=selected_folder)

    management_name = 'Edit Folder'

    management_icon = Icon.objects.filter(name='folder').first()
    
    action_url = reverse('edit_folder', args=(folder.name, selected_folder.name))

    sub_folders = Folder.objects.filter(parent_folder=folder).order_by('-created_at')

    resources = Resource.objects.filter(folder=folder).order_by('-created_at')

    parent_folders = get_parent_folders(folder)

    parent_folders.reverse()

    if not (sub_folders or resources):
        no_resources_or_folders = True
    else:
        no_resources_or_folders = False

    context = {
        'form': form,
        'folder': folder,
        'selected_folder': selected_folder,
        'sub_folders': sub_folders,
        'resources': resources,
        'parent_folders': parent_folders,
        'no_resources_or_folders': no_resources_or_folders,
        'management_name': management_name,
        'management_icon': management_icon,
        'action_url': action_url,
        'delete_btn': True,
    }

    return render(request, 'resources/folder_management.html', context)


@login_required
def delete_folder(request, folder_name, selected_folder_name):

    user = request.user

    if not user.is_superuser:
        messages.error(request, "You must be an admin to delete a folder!")
        return redirect(reverse('home'))
    
    folder = Folder.objects.filter(name=folder_name).first()

    if folder:
        redirect_url = reverse('folder', args=(folder.name,))
    else:
        redirect_url = reverse('resources')

    selected_folder = Folder.objects.filter(name=selected_folder_name).first()

    if not selected_folder:
        messages.error(request, "Invalid folder!")
        return redirect(redirect_url)
    
    selected_folder.delete()

    messages.success(request, "Successfully deleted folder!")
    return redirect(redirect_url)

