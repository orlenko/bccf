from django.db.models import get_model, ObjectDoesNotExist, Q
from mezzanine import template

from bccf.models import BCCFChildPage, UserProfile

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
    context['class'] = 'hpro'
    context['slides'] = BCCFChildPage.objects.filter(content_model='program', featured=True).order_by('-created')
    return context
    
@register.inclusion_tag('generic/includes/featured.html', takes_context=True)
def featured_tags(context):
    """
    Provides a generic context variable name for the TAGs to be shown on the front page
    """
    context['class'] = 'hnote'
    context['slides'] = BCCFChildPage.objects.filter(Q(content_model='formpublished', featured=True) | Q(content_model='topic', featured=True) | Q(content_model='campaign', featured=True))
    return context
    
@register.inclusion_tag('generic/includes/featured_resources.html', takes_context=True)
def featured_resources(context):
    """
    Provides a generic context variable name for the featured resources to be shown on the front page
    """
    context['slides'] = BCCFChildPage.objects.filter(Q(content_model='article', featured=True) | Q(content_model='downloadableform', featured=True) | Q(content_model='magazine', featured=True) | Q(content_model='tipsheet', featured=True) | Q(content_model='video', featured=True)).order_by('-created')
    return context
    
@register.inclusion_tag('generic/includes/featured_users.html', takes_context=True)
def featured_users(context, type): # 0 - level 1; 50 - level 2; 100 - level 3
    context['users'] = UserProfile.objects.filter(membership_type=type, membership_level=100).order_by('?')
    return context