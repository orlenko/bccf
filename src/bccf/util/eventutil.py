import logging
log = logging.getLogger(__name__)

from decimal import Decimal
from dateutil.relativedelta import relativedelta

from django.utils.timezone import now
from django.contrib.auth.models import User

from cartridge.shop.models import Cart, ProductVariation

from bccf.models import Event, EventRegistration
from bccf.models import Settings

def show_bill(request):
    """
    Checks whether or not an event is in the cart and returns false if the
    start date of the event is less than 2 weeks from now.
    
    False means that paypal is the only good method of payment.
    True means the bill method of payment is fine.
    """
    cart = Cart.objects.from_request(request)
    for order_item in cart.items.all():
        if order_item.sku.startswith('EVENT-'):
            sku_parts = order_item.sku.split('EVENT-')
            event = Event.objects.get(id=int(sku_parts[1]))
            start = event.date_start
            limit = start - relativedelta(days=14)
            return limit > now()
        if order_item.sku.startswith('ORG') or order_item.sku.startswith('PRO'):
            return False
    return True
    
def handle_event(request, user, order):
    """
    Check if the order has events in it. Process the even and register
    the user.
    """
    for order_item in order.items.all():
        variation = ProductVariation.objects.get(sku=order_item.sku)
        if order_item.sku.startswith('EVENT-'):
            sku_parts = order_item.sku.split('EVENT-')
            event = Event.objects.get(id=int(sku_parts[1]))
            paid = False
            
            # If payment is paypal everything is good!
            if order.payment_method == 'paypal':
                order.status = 2
                order.save()
                paid = True
                
                # Adds a the payment to the total payment for the professional after a cut
                if not event.provider.is_superuser:
                    cut = event.price * Decimal(Settings.get_setting('BCCF_PERCENTAGE_CUT'))
                    price = event.price - cut
                    profile = event.provider.profile
                    if not profile.payment:
                        profile.payment = price
                    else:
                        profile.payment += price
                    profile.save()    
                    
            if user.profile.is_organization:
                user_ids = request.session.get('register_selected_members', [])
                event_id = request.session.get('register_selected_event', None)
                
                if not event_id:
                    log.debug('event ID is None')
                    return
                    
                event = Event.objects.get(id=event_id)
                for user_id in user_ids:
                    u = User.objects.get(id=user_id)
                    EventRegistration.objects.create(user=user, event=event,
                                            event_order=order, paid=paid)
                                            
                del request.session['register_selected_members']
                del request.session['register_selected_event']
                                    
            else:        
                EventRegistration.objects.create(user=user, event=event, 
                                         event_order=order, paid=paid)

            return