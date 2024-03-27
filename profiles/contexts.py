from .models import UserProfile


def profile(request):
    profile = None
    num_of_classes = 0
    if request.user.is_authenticated:
        profile = UserProfile.objects.filter(user=request.user).first()


    context = {
        'profile': profile,
        'number_of_classes': num_of_classes
    }
    return context