from django.shortcuts import render, redirect, reverse
from .models import Resource, ResourceType, Folder
from django.contrib.auth.decorators import login_required
from membership.models import Membership


@login_required
def quick_resources(request):

    user = request.user

    membership = Membership.objects.get(user=user)

    if membership:
        if not membership.status.valid:
            return redirect(reverse('membership'))
    else:
        return redirect(reverse('membership'))
    
    folder = Folder.objects.get(name='all_resources')

    sub_folders = Folder.objects.filter(parent_folder=folder)

    resources = Resource.objects.filter(folder=folder)

    context = {
        'folder': folder,
        'sub_folders': sub_folders,
        'resources': resources,
    }

    return render(request, 'resources/quick_resources.html', context)


@login_required
def all_resources(request):

    user = request.user

    membership = Membership.objects.get(user=user)

    if membership:
        if not membership.status.valid:
            return redirect(reverse('membership'))
    else:
        return redirect(reverse('membership'))
    
    folder = Folder.objects.get(name='all_resources')

    sub_folders = Folder.objects.filter(parent_folder=folder)

    resources = Resource.objects.filter(folder=folder)

    return_url = reverse('quick_resources')

    context = {
        'folder': folder,
        'sub_folders': sub_folders,
        'resources': resources,
        'return_url': return_url,
    }

    return render(request, 'resources/resources.html', context)


def folder(request, folder_name):

    user = request.user

    membership = Membership.objects.get(user=user)

    if membership:
        if not membership.status.valid:
            return redirect(reverse('membership'))
    else:
        return redirect(reverse('membership'))
    
    folder = Folder.objects.get(name=folder_name)

    sub_folders = Folder.objects.filter(parent_folder=folder)

    resources = Resource.objects.filter(folder=folder)

    if folder_name == 'all_resources':
        return_url = reverse('quick_resources')
    else:
        return_url = reverse('folder', args=(folder.parent_folder.name,))

    context = {
        'folder': folder,
        'sub_folders': sub_folders,
        'resources': resources,
        'return_url': return_url,
    }

    return render(request, 'resources/resources.html', context)
