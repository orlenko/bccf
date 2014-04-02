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
    
    # Makes sure that the prices have two decimal places    
    TWO_PLACES = Decimal(10) ** -2
    
    discount = ''
    if order.discount_total:
        discount = str(Decimal(order.discount_total).quantize(TWO_PLACES))

    data = order_form.cleaned_data

    payment = paypal.Payment({
        'intent': 'sale',
        'payer': {
            'payment_method': 'paypal',
        },
        'transactions': [{
            'item_list': {
                'items': items,
                #'shipping_address': {
                #    'recipient_name': '%s %s' % (data['shipping_detail_first_name'], data['shipping_detail_last_name']),
                #    'line1': data['shipping_detail_street'],
                #    'city': data['shipping_detail_city'],
                #    'country_code': data['shipping_detail_country'],
                #    'postal_code': data['shipping_detail_postcode'],
                #    'state': data['shipping_detail_state'],
                #    'phone': data['shipping_detail_phone'],
                #},
            },
            'amount': {
                'total': str(Decimal(order.total).quantize(TWO_PLACES)),
                'currency': 'CAD',
                'details': {
                    'subtotal': str(cart.total_price()),
                    'tax': str(Decimal(order.tax_total).quantize(TWO_PLACES)),
                    'shipping': str(Decimal(order.shipping_total).quantize(TWO_PLACES)),
                    #'discount': discount, 
                },
            },
            'description': 'Invoice for BCCF Registration/Product Purchases'
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
        request.session['paypal_id'] = payment.id
        
        log.debug(payment)
        # payment.does_not_exist()
        
        # Return redirect URL
        for link in payment.links:
            if link.method == "REDIRECT":
                log.debug("Approve URL: %s" % link.href)
                return link.href
    else:
        raise CheckoutError(payment.error)

def execute(request, payer_id):
    paypal_id = request.session["paypal_id"]
    payment = paypal.Payment.find(paypal_id)
    
    if payment.execute({"payer_id": payer_id}):
        return True
    else:
        raise CheckoutError(payment.error)
        
def find(request):
    paypal_id = request.session["paypal_id"]
    return paypal.Payment.find(paypal_id)