from django.http import HttpResponse
import json
import stripe

def stripe_webhook(request):
    payload = request.body
    sig_header = request.headers['Stripe-Signature']
    endpoint_secret = "your_stripe_webhook_secret_key"  # Replace with your webhook secret key
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    
    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        # Handle successful payment
        handle_successful_payment(event)
    elif event['type'] == 'payment_intent.payment_failed':
        # Handle failed payment
        handle_failed_payment(event)
    # Add more event types as needed
    
    return HttpResponse(status=200)