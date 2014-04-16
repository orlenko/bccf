import httplib2
import logging
import paypalrestsdk as paypal
from decimal import Decimal
log = logging.getLogger(__name__)

from django.core.exceptions import ImproperlyConfigured

from cartridge.shop.models import Cart, DiscountCode
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

def process(request, order_form):
    """
    Uses the REST API of Paypal to create a direct purchase payment according the entered
    Credit Card Number and Billing Information.
    """
    cart = Cart.objects.from_request(request)
    items = []
    tax = Decimal(request.session.get('tax_total', 0))
    shipping = Decimal(request.session.get('shipping_total', 0))
    total = tax + shipping
    subtotal = Decimal(0)
    
    discount = code = order_form._request.session.get('discount_code', None)
    if code:
        try:
            discount = DiscountCode.objects.get(code=discount)
        except:
            log.debug("code doesn't exist")
   
    # Create a list of items to be sent to paypal
    for item in cart.items.all():
        price = item.unit_price
        if discount: # Dicounted?
            price -= cart.calculate_item_discount(item, discount)
        subtotal += price
        items.append({
            'name': 'item',
            'sku': item.sku,
            'price': str(price),
            'currency': 'CAD',
            'quantity': item.quantity
        })
        
    total += subtotal   
    
    # Makes sure that the prices have two decimal places    
    TWO_PLACES = Decimal(10) ** -2

    #data = order_form.cleaned_data

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
                'total': str(total.quantize(TWO_PLACES)),
                'currency': 'CAD',
                'details': {
                    'subtotal': str(subtotal.quantize(TWO_PLACES)),
                    'tax': str(tax.quantize(TWO_PLACES)),
                    'shipping': str(shipping.quantize(TWO_PLACES)),
                },
            },
            'description': 'Invoice for BCCF Registration/Product Purchases'
        }],
        'redirect_urls': {
            'return_url': PAYPAL_RETURN_URLS,
            'cancel_url': PAYPAL_CANCEL_URLS       
        },
    })

    if payment.create(): # Success
        request.session['paypal_id'] = payment.id
        # Return redirect URL
        for link in payment.links:
            if link.method == "REDIRECT":
                log.debug("Approve URL: %s" % link.href)
                return link.href
    else:
        raise CheckoutError(payment.error)

def execute(request):
    paypal_id = request.session.get("paypal_id", None)
    payer_id = request.GET.get("PayerID", None)
    
    if not paypal_id and not payer_id:
        return False
    
    payment = paypal.Payment.find(paypal_id)
    
    if payment.execute({"payer_id": payer_id}):
        return True
    else:
        raise CheckoutError(payment.error)
        
def find(request):
    paypal_id = request.session["paypal_id"]
    return paypal.Payment.find(paypal_id)