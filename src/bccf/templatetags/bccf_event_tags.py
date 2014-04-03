import simplejson

from django.db.models import get_model, ObjectDoesNotExist, Q
from mezzanine import template

from cartridge.shop.forms import AddProductForm

from bccf.models import BCCFChildPage, Event, EventRegistration

import logging
import re

log = logging.getLogger(__name__)

register = template.Library()


@register.inclusion_tag("generic/includes/subscribe.html", takes_context=True)
def bccf_subscribe_for(context, obj):
    """If obj is subscribable (like an event), render a form for subscribing to it.
    """
    if obj._meta.object_name == 'BCCFChildPage':
        if obj.content_model == 'event':
            context['subscribe_obj'] = obj
            context['event_obj'] = obj.get_content_model()
            context['product'] = obj.get_content_model().event_product
    return context
    
@register.inclusion_tag("generic/includes/attendee_list.html", takes_context=True)
def attendees_for(context, event):
    context['attendees'] = EventRegistration.objects.filter(event=event)
    context['event_obj'] = event.get_content_model()
    return context
    
@register.inclusion_tag("generic/includes/user_event.html", takes_context=True)
def events_of(context, user):
    if user.is_level_C:
        context['event_objs'] = Event.objects.filter(provider=user).order_by('-date_start')[:5]
    return context