from django.shortcuts import render, redirect, get_object_or_404


def members(request):
    return render(request, 'members/members.html')