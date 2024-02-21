from django.shortcuts import render, redirect, reverse
from .models import Membership, MembershipPackage, MembershipStatus
from .forms import MembershipPackageForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required


@login_required
def membership_redirect(request):
    user = request.user
    membership = Membership.objects.filter(user=user).first()

    if request.method == "POST":
        form = MembershipPackageForm(request.POST)

        if form.is_valid():
            package_name = form.cleaned_data["package_name"]
            
            membership_package = MembershipPackage.objects.get(name=package_name)

            if not membership:
                membership_status = MembershipStatus.objects.get(name="pending")
                membership = Membership.objects.create(user=user, status=membership_status, package=membership_package)
            else:
                if membership.is_valid:
                    membership_status = MembershipStatus.objects.get(name="active_renewal_pending")
                else:
                    membership_status = MembershipStatus.objects.get(name="pending")
                membership.package = membership_package
                membership.status = membership_status
                membership.save()

            request.session['membership_redirect_success'] = True

            return redirect(reverse('membership_redirect_success'))  # Redirect to success page
    else:
        form = MembershipPackageForm()

    all_membership_packages = MembershipPackage.objects.all()

    if all_membership_packages.count() == 1:
        single_membership_package = all_membership_packages.first()
    else:
        single_membership_package = False

    if membership:
        heading_text = "Membership Renewal"
        if membership.end_date:
            membership_duration_left = membership.end_date - timezone.now().date()
            duration_left_in_days = membership_duration_left.days
        else:
            duration_left_in_days = 0

        if (membership.status.name == "active" and duration_left_in_days > 60) or (membership.status.name == "pending") or (membership.status.name == "active_renewal_pending"):
            return redirect(reverse('membership_status'))
    else:
        heading_text = "Account Setup!"

    context = {
            'form': form,
            'membership_packages': all_membership_packages,
            'single_membership_package': single_membership_package,
            'heading_text': heading_text,
        }
    return render(request, 'membership/membership_redirect.html', context)


@login_required
def membership_redirect_success(request):

    # if not request.session.get('membership_redirect_success'):
    #     return redirect(reverse('membership_status'))
    
    user = request.user

    membership = Membership.objects.filter(user=user).first()

    if membership.status.name == 'active_renewal_unsuccessful' or membership.status.name == 'active_renewal_pending':
        split_status_friendly_name = membership.status.friendly_name.split(' - ')
        active_status = split_status_friendly_name[0]
        renewal_status = split_status_friendly_name[1].split(' ')[1]
    else:
        active_status = False
        renewal_status = False

    checkout_url = membership.package.checkout_url

    context = {
        'membership': membership,
        'checkout_url': checkout_url,
        'renewal_button': False,
        'active_status': active_status,
        'renewal_status': renewal_status,
    }

    # del request.session['membership_redirect_success']

    return render(request, 'membership/membership_status.html', context)


@login_required
def membership_status(request):

    user = request.user

    membership = Membership.objects.filter(user=user).first()

    if membership.status.name == 'active_renewal_unsuccessful' or membership.status.name == 'active_renewal_pending':
        split_status_friendly_name = membership.status.friendly_name.split(' - ')
        active_status = split_status_friendly_name[0]
        renewal_status = split_status_friendly_name[1].split(' ')[1]
    else:
        active_status = False
        renewal_status = False


    if membership.end_date:
        membership_duration_left = membership.end_date - timezone.now().date()
        duration_left_in_days = membership_duration_left.days
    else:
        duration_left_in_days = 0

    if membership.status.name == 'expired' or membership.status.name == 'canceled' or membership.status.name == 'payment_unsuccessful' or ((membership.status.name == 'active' or membership.status.name == 'active_renewal_unsuccessful') and duration_left_in_days < 60):
        if membership.start_date:
            renewal_button = "Renew"
        else:
            renewal_button = "Purchase"
        
    else:
        renewal_button = False

    context = {
        'membership': membership,
        'renewal_button': renewal_button,
        'active_status': active_status,
        'renewal_status': renewal_status,
    }

    return render(request, 'membership/membership_status.html', context)


@login_required
def membership_cancel(request):
    if request.method == 'POST':
        # Check if the cancel button was clicked
        if 'cancel_membership' in request.POST:
            user = request.user
            membership = Membership.objects.filter(user=user).first()

            if membership:
                # Update membership status to canceled
                cancel_status = MembershipStatus.objects.get(name="canceled")
                membership.status = cancel_status
                membership.save()
                return redirect(reverse("membership_redirect"))
    
    # If the request is not a POST or the cancel button wasn't clicked, redirect to membership status
    return redirect(reverse('membership_status'))
