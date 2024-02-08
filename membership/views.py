from django.shortcuts import render, redirect, reverse


def membership_payment(request):

    if request.method == 'POST':
        message = request.POST.get('mock_message')
        if message == 'y':
            return redirect(reverse('membership_payment_success'))
        else:
            return redirect(reverse('membership_payment'))
    else:
        return render(request, 'membership/membership_payment.html')
    

def membership_payment_success(request):
    return render(request, 'membership/membership_payment_success.html')
