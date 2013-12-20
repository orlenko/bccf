from django.db.models import get_model, ObjectDoesNotExist, Q
from mezzanine import template

from bccf.models import BCCFChildPage

import logging
import re

log = logging.getLogger(__name__)

register = template.Library()

@register.inclusion_tag("generic/includes/featured.html", takes_context=True)
def featured_programs(context):
    """
    Provides a generic context variable name for the object that carousels are
    being rendered for.
    """
    context['slides'] = BCCFChildPage.objects.filter(content_model='program', featured=True).order_by('-created')
    return context
    
def featured_tag(context):
    pass
    
@register.inclusion_tag('generic/includes/featured_resources.html', takes_context=True)
def featured_resources(context):
    context['slides'] = BCCFChildPage.objects.filter(Q(content_model='article', featured=True) | Q(content_model='downloadableform', featured=True) | Q(content_model='magazine', featured=True) | Q(content_model='tipsheet', featured=True) | Q(content_model='video', featured=True)).order_by('-created')
    log.info(context['slides'])
    return context;
    
def resources_for(context, topic=None):
    pass