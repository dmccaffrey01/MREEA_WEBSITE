from django.shortcuts import render, redirect, reverse
from .models import Notification
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from membership.models import Membership


@require_POST
@login_required
def add_notification(request):
    if request.method == 'POST':
        user = request.user

        # Get post data (heading, message, important_status)
        heading = request.POST.get('heading')
        message = request.POST.get('message')
        important_status = request.POST.get('important_status')

        # Your logic to handle the notification creation
        
        # Example response data
        response_data = {
            'success': True,
            'message': 'Notification added successfully.'
        }
        return JsonResponse(response_data, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


@login_required
def mark_notification_as_read(request, sku):

    user = request.user



    return True