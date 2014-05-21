from django.db.models import get_model, ObjectDoesNotExist, Q
from mezzanine import template

from bccf.models import BCCFChildPage, Program, UserProfile

import logging
import re
import datetime

log = logging.getLogger(__name__)

register = template.Library()

BCCF_EXPIRY = Q(expiry_date__gte=datetime.datetime.now()) | Q(expiry_date=None)
BCCF_FILTER = {
    'status': 2,
    'publish_date__lte': datetime.datetime.now(),
    'featured': True
}

@register.inclusion_tag("generic/includes/featured.html", takes_context=True)
def featured_programs(context):
    """
    Provides a generic context variable name for the object that carousels are
    being rendered for.
    """
    context['class'] = 'hpro'
    context['slides'] = Program.objects.published().filter(featured=True).order_by('-created')
    return context
    
@register.inclusion_tag('generic/includes/featured.html', takes_context=True)
def featured_tags(context):
    """
    Provides a generic context variable name for the TAGs to be shown on the front page
    """
    context['class'] = 'hnote'
    context['slides'] = BCCFChildPage.objects.published().filter(Q(content_model='formpublished') | Q(content_model='topic') | Q(content_model='campaign'), featured=True).order_by('-created')
    return context
    
@register.inclusion_tag('generic/includes/featured_resources.html', takes_context=True)
def featured_resources(context):
    """
    Provides a generic context variable name for the featured resources to be shown on the front page
    """
    context['slides'] = BCCFChildPage.objects.filter(Q(content_model='article') | Q(content_model='downloadableform') | Q(content_model='magazine') | Q(content_model='podcast') | Q(content_model='tipsheet') | Q(content_model='video'), BCCF_EXPIRY, **BCCF_FILTER).order_by('-created')
    return context
    
@register.inclusion_tag('generic/includes/featured_users.html', takes_context=True)
def featured_users(context, type): # 0 - level 1; 50 - level 2; 100 - level 3
    context['users'] = UserProfile.objects.get_directory().filter(membership_type=type, membership_level='C').order_by('?')
    return context
    
@register.inclusion_tag('generic/related_resources.html', takes_context=True)
def related_resources_for(context, obj, type, title):
    context['resource_type'] = title
    #Related resources
    q = Q()
    for topic in obj.bccf_topic.all():
        q = q | Q(bccf_topic = topic)
        
    resource_pre = BCCFChildPage.objects.published().filter(Q(content_model=type)).distinct()
    context['resources'] = resource_pre.filter(q, ~Q(slug=obj.slug)).order_by('featured', '-created')[:10]
    return context