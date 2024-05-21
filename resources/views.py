from django.shortcuts import render, redirect, reverse
from .models import Resource, Folder
from django.contrib.auth.decorators import login_required
from membership.models import Membership


@login_required
def resources(request):

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

    parent_folders = get_parent_folders(folder)

    parent_folders.reverse()

    context = {
        'folder': folder,
        'sub_folders': sub_folders,
        'resources': resources,
        'parent_folders': parent_folders,
    }

    return render(request, 'resources/resources.html', context)


def get_parent_folders(folder, arr=None):
    if arr is None:
        arr = []
        
    new_arr = list(arr)
    
    new_arr.append(folder)

    if folder.name == 'all_resources':
        return new_arr
    else:
        parent_folder = folder.parent_folder
        if parent_folder:
            return get_parent_folders(parent_folder, new_arr)
        else:
            return new_arr
