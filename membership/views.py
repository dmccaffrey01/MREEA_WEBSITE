from django.shortcuts import render, redirect, reverse
from .models import Membership, MembershipPackage, MembershipStatus
from .forms import MembershipPackageForm, MembershipForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from profiles.models import UserProfile


@login_required
def membership_redirect(request):
    user = request.user
    membership = Membership.objects.filter(user=user).first()

    request.session['membership_redirect_success'] = False

    if request.method == "POST":
        form = MembershipPackageForm(request.POST)

        if form.is_valid():
            package_name = form.cleaned_data["package_name"]
            
            membership_package = MembershipPackage.objects.filter(name=package_name).first()

            if not membership:
                membership = Membership.objects.create(user=user)
            if membership.is_valid():
                membership_status = MembershipStatus.objects.filter(name="active_renewal_pending").first()
            else:
                membership_status = MembershipStatus.objects.filter(name="pending").first()
            membership.package = membership_package
            membership.status = membership_status
            membership.make_pending()
            membership.save()

            request.session['membership_redirect_success'] = True

            message = 'Successfully Selected Package!'
            messages.success(request, message)

            return redirect(reverse('membership_redirect_success'))  # Redirect to success page
    else:
        form = MembershipPackageForm()

    all_membership_packages = MembershipPackage.objects.all().exclude(name="admin_membership").exclude(name="hidden_admin_membership")

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
            message = 'Redirected to Membership Status'
            messages.info(request, message)
            return redirect(reverse('membership_status'))
    else:
        heading_text = "Account Setup!"

    message = 'Select Membership Package'
    messages.info(request, message)

    context = {
            'form': form,
            'membership_packages': all_membership_packages,
            'single_membership_package': single_membership_package,
            'heading_text': heading_text,
        }
    return render(request, 'membership/membership_redirect.html', context)


@login_required
def membership_redirect_success(request):

    if not request.session.get('membership_redirect_success'):
        message = 'Redirected to Membership Status'
        messages.info(request, message)
        return redirect(reverse('membership_status'))
    
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

    return render(request, 'membership/membership_redirect_success.html', context)


@login_required
def membership_status(request):

    user = request.user

    membership = Membership.objects.filter(user=user).first()

    if not membership:
        return redirect(reverse('membership_redirect')) 

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

    if membership.status.name == 'expired' or membership.status.name == 'active_renewal_unsuccessful' or (membership.status.name == 'active' and duration_left_in_days < 60):
        renewal_button = "Renew"
    elif membership.status.name == 'canceled' or membership.status.name == 'payment_unsuccessful':
        renewal_button = "Purchase"
    else:
        renewal_button = False
    
    if request.session.get('membership_redirect_success'):
        message = 'Successfully Applied for Membership!'
        messages.success(request, message)
        del request.session['membership_redirect_success']


    context = {
        'membership': membership,
        'renewal_button': renewal_button,
        'active_status': active_status,
        'renewal_status': renewal_status,
    }

    return render(request, 'membership/membership_status.html', context)


@login_required
def membership_management(request, username):

    user = request.user

    if not user.is_superuser:
        messages.error(request, "You must be an admin to continue!")
        return redirect(reverse('home'))
    
    selected_user = User.objects.filter(username=username).first()

    if not selected_user:
        messages.error(request, "Invalid user")
        return redirect(reverse('members_management'))
    
    selected_profile = UserProfile.objects.filter(user=selected_user).first()

    if not selected_profile:
        messages.error(request, "Invalid user profile")
        return redirect(reverse('membership_management'))
    
    selected_membership = Membership.objects.filter(user=selected_user).first()

    if not selected_membership:
        messages.error(request, "Invalid membership")
        return redirect(reverse('membership_management'))
    
    if request.method == 'POST':
        form = MembershipForm(request.POST)

        if form.is_valid():
            form_data = form.cleaned_data
            purchase_date = form_data['purchase_date']
            start_date = form_data['start_date']
            end_date = form_data['end_date']

            package_name = request.POST.get('id_package_name')
            status_name = request.POST.get('id_status_name')

            membership_package = MembershipPackage.objects.filter(name=package_name).first()
            membership_status = MembershipStatus.objects.filter(name=status_name).first()

            selected_membership.package = membership_package
            selected_membership.status = membership_status
            selected_membership.status_name = status_name
            selected_membership.purchase_date = purchase_date
            selected_membership.start_date = start_date
            selected_membership.end_date = end_date
            selected_membership.save()

            messages.success(request, "Successfully updated membership!")
            return redirect(reverse('members_management'))
        else:
            for error in form.errors:
                print(error)

    else:
        form = MembershipForm(instance=selected_membership)
    
    membership_packages = MembershipPackage.objects.all()
    membership_statuses = MembershipStatus.objects.all()
    
    context = {
        'form': form,
        'selected_profile': selected_profile,
        'selected_membership': selected_membership,
        'membership_packages': membership_packages,
        'membership_statuses': membership_statuses,
    }

    return render(request, 'management/membership_management.html', context)
