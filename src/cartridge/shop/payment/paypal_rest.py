import httplib2
import logging
import paypalrestsdk as paypal
from decimal import Decimal
log = logging.getLogger(__name__)

from django.core.exceptions import ImproperlyConfigured

from cartridge.shop.models import Cart
from cartridge.shop.checkout import CheckoutError

from bccf import settings

try:
    PAYPAL_MODE = settings.PAYPAL_MODE
    PAYPAL_CLIENT_ID = settings.PAYPAL_CLIENT_ID
    PAYPAL_CLIENT_SECRET = settings.PAYPAL_CLIENT_SECRET
    PAYPAL_RETURN_URLS = settings.PAYPAL_RETURN_URLS
    PAYPAL_CANCEL_URLS = settings.PAYPAL_CANCEL_URLS
except AttributeError:
    raise ImproperlyConfigured("You need to define PAYPAL_MODE, "
                               "PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET, "
                               "PAYPAL_RETURN_URLS and PAYPAL_CANCEL_URLS "
                               "in your settings module to use the "
                               "paypal payment processor.")
                               
paypal.configure({
    'mode': PAYPAL_MODE,
    'client_id': PAYPAL_CLIENT_ID,
    'client_secret': PAYPAL_CLIENT_SECRET
})

def process(request, order_form, order):
    """
    Uses the REST API of Paypal to create a direct purchase payment according the entered
    Credit Card Number and Billing Information.
    """
    cart = Cart.objects.from_request(request)
    items = []
    
    # Create a list of items to be sent to paypal
    for item in cart.items.all():
        items.append({
            'name': 'item',
            'sku': item.sku,
            'price': str(item.unit_price),
            'currency': 'CAD',
            'quantity': item.quantity
        })
        
    log.debug(order.total)
    log.debug(order.tax_total)
    log.debug(order.shipping_total)        
        
    payment = paypal.Payment({
        'intent': 'sale',
        'payer': {
            'payment_method': 'paypal',   
        },
        'transactions': [{
            'item_list': {
                'items': items
            },
            'amount': {
                'total': str(order.total),
                'currency': 'CAD',
                'details': {
                    'subtotal': str(cart.total_price()),
                    'tax': str(order.tax_total),
                    'shipping': str(order.shipping_total)       
                }  
            },
            'description': 'Test Payment'
        }],
        'redirect_urls': {
            'return_url': PAYPAL_RETURN_URLS,
            'cancel_url': PAYPAL_CANCEL_URLS       
        },
    })
    
    # Uncomment to produce an error
    # payment.does_not_exist()

    if payment.create(): # Success
        log.debug("Payment Successful: %s" % payment.id)
        # Return redirect URL
        for link in payment.links:
            if link.method == "REDIRECT":
                log.debug("Approve URL: %s" % link.href)
                return link.href
    else:
        raise CheckoutError(payment.error)
