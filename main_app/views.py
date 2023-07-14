import os
import requests
from django.shortcuts import render, redirect
import json
from django.http import JsonResponse
from django.db.models import Q
from .forms import CustomSignupForm
from django.contrib.auth import login
from django.shortcuts import render, redirect


previous_url = '/'


def index(request):
    global previous_url
    
    previous_url = '/'

    context = {
        
    }

    return render(request, 'index.html', context)


def membership(request):
    global previous_url
    
    user = request.user

    previous_url = '/membership/'
    print(previous_url)

    logged_in = user.is_authenticated

    context = {
        'logged_in': logged_in,
    }

    return render(request, 'membership.html', context)



def signup_view(request):
    global previous_url
    if previous_url.endswith('/membership/'):
        membership = True
    else:
        membership = False

    print(previous_url)
    print(previous_url)
    print(previous_url)

    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save(request)
            login(request, user)
            
            if previous_url:
                return redirect(previous_url)
            else:
                return redirect('home')
    else:
        form = CustomSignupForm()
    
    return render(request, 'account/signup.html', {
        'form': form,
        'membership': membership,
    })