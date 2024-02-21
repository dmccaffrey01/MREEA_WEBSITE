from .models import Membership

def membership_context(request):
    user = request.user
    membership = None
    is_membership_valid = False
    if user.is_authenticated:
        # Retrieve the user's membership model if it exists
        try:
            membership = Membership.objects.get(user=user)
            is_membership_valid = membership.is_valid
        except Membership.DoesNotExist:
            membership = None
    else:
        membership = None

    context = {
        'membership': membership,
        'is_membership_valid': is_membership_valid,
    }
    return context