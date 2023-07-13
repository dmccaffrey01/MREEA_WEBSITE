import os
import requests
from django.shortcuts import render
import json
from django.http import JsonResponse
from django.db.models import Q


def index(request):
    
    context = {
        
    }

    return render(request, 'index.html', context)
