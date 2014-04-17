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
    profile = None
    request = context['request']
    user = request.user
    if user.is_authenticated():
        profile = user.profile
    if obj._meta.object_name == 'BCCFChildPage':
        if obj.content_model == 'event':
            context['subscribe_obj'] = obj 
            event = obj.get_content_model()
            context['event_for'] = event.page_for
            if profile:
                if event.page_for == profile.membership_type \
                    or (event.page_for == 'professional' and profile.membership_type != 'parent'):
                    context['event_obj'] = event
    return context
    
@register.inclusion_tag("generic/includes/short_subscribe.html", takes_context=True)
def bccf_short_subscribe_for(context, obj, li_class=None):
    """
    Short version of the subscribe_for that will be used for event tables.
    """
    context['li_class'] = li_class
    profile = None
    request = context['request']
    user = request.user
    if user.is_authenticated():
        profile = user.profile   
    if obj._meta.object_name == 'Event':
        event = obj
        if profile:
            if event.page_for == profile.membership_type \
                or (event.page_for == 'professional' and profile.membership_type != 'parent'):
                context['event_obj'] = event
    return context
    
@register.inclusion_tag("generic/includes/attendee_list.html", takes_context=True)
def attendees_for(context, event):
    context['attendees'] = EventRegistration.objects.filter(event=event)
    context['event_obj'] = event.get_content_model()
    return context
    
@register.inclusion_tag("generic/includes/user_event.html", takes_context=True)
def events_of(context, user, in_pro=False):
    context['in_pro'] = in_pro
    context['user_url'] = user.get_absolute_url();
    if user.is_level_C:
        context['event_objs'] = Event.objects.user_event_list(user).order_by('date_start')[:5]
    return context