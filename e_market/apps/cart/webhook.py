from itertools import product
import json
import stripe

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .cart import Cart

from apps.order.models import Order
#from apps.store.utilities import decrement_product_quantity, send_order_confirmation

@csrf_exempt
def webhook(request):
    payload = request.body
    event = None

    stripe.api_key = settings.STRIPE_API_KEY_HIDDEN

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        return HttpResponse(status=400)

    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object
        print('Payment intent', payment_intent.id)
        
        order = Order.objects.get(payment_intent=payment_intent.id)
        order.paid = True
        order.save()

        for item in order.item.all():
            product = item.product
            product.num_available = product.num_available -item.quantity
            product.save()

        """ decrement_product_quantity(order)  
        send_order_confirmation(order) """
        
    return HttpResponse(status=200)