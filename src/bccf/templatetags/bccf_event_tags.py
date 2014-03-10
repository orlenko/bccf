from django.db.models import get_model, ObjectDoesNotExist, Q
from mezzanine import template

from bccf.models import BCCFChildPage, EventRegistration

import logging
import re

log = logging.getLogger(__name__)

register = template.Library()


@register.inclusion_tag("generic/includes/subscribe.html", takes_context=True)
def bccf_subscribe_for(context, obj):
    """If obj is subscribable (like an event), render a form for subscribing to it.
    """
    log.debug('Checking subscribe form for %s' % obj._meta.object_name)
    if obj._meta.object_name == 'BCCFChildPage':
        if obj.content_model == 'event':
            log.debug('Subscribe form leads to %s' % obj.get_content_model().signup_url())
            context['subscribe_obj'] = obj.get_content_model()
    return context
    
@register.inclusion_tag("generic/includes/attendee_list.html", takes_context=True)
def attendees_for(context, event):
    context['attendees'] = EventRegistration.objects.filter(event=event)
    context['event_obj'] = event.get_content_model()
    return context