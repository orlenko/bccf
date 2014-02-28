from django.db.models import get_model, ObjectDoesNotExist, Q
from mezzanine import template
from mezzanine.pages.models import Page

from bccf.models import BCCFChildPage, BCCFPage

import logging
import re
import datetime

log = logging.getLogger(__name__)

BCCF_EXPIRY = Q(expiry_date__gte=datetime.datetime.now()) | Q(expiry_date=None)

register = template.Library()

@register.inclusion_tag("generic/includes/content_carousel.html", takes_context=True)
def product_category_carousel(context, category):
    page = re.split('/get/', context['request'].path)
    params = None
    context['open'] = False
    context['filter'] = False
    context['carousel_color'] = category.get_content_model().carousel_color
    context['carousel_title'] = category.title
    context['carousel_name'] = 'products'
    context['slides'] = category.get_content_model().products.all()
    return context

@register.inclusion_tag("generic/includes/content_carousel.html", takes_context=True)
def content_carousel_for(context, obj, title, child=None, which=None):
    """
    Provides a generic context variable name for the object that carousels are
    being rendered for.
    """
    page = re.split('/get/', context['request'].path)
    params = None
    context['open'] = False
    context['filter'] = False
    context['carousel_color'] = obj.get_content_model().carousel_color
    context['carousel_title'] = title
    context['carousel_name'] = which
    context['slides'] = None
    
    filter = {
        'gparent': obj,
        'status': 2,
        'publish_date__lte': datetime.datetime.now(),
    }

    if title == 'Talk':
        context['filter'] = True
    try:
        if which:
            if obj.slug == 'bccf/resources' or obj.slug == 'bccf/tag':
                filter['content_model'] = which
            else:
                filter['page_for'] = which
        if child:
            temp = BCCFChildPage.objects.get(slug=child)
            context['open'] = True
            context['slides'] = [temp]
            context['slides'].extend(BCCFChildPage.objects.filter(~Q(slug=child), BCCF_EXPIRY, **filter).order_by('-created')[:11])
        else:
            context['slides'] = BCCFChildPage.objects.filter(BCCF_EXPIRY, **filter).order_by('-created')[:12]
            
    except ObjectDoesNotExist, e:
        log.info('Object Does Not Exist')
        log.error(e)
    except Exception, e:
        log.info('Unspecified Exception')
        log.error(e)
        return
    return context

@register.inclusion_tag("generic/includes/content_carousel.html", takes_context=True)
def content_carousel_for_topic(context, topic, type):
    """
    The same a the content carousel_for but this focuses on all pages that are related to a Topic
    """
    filter = {
        'status': 2,
        'publish_date__lte': datetime.datetime.now(),
        'bccf_topic': topic,
        'page_for': type
    }

    try:
        context['slides'] = BCCFChildPage.objects.filter(BCCF_EXPIRY, **filter).order_by('-created')[:12]
        context['carousel_color'] = topic.carousel_color
        context['carousel_title'] = type
        context['carousel_name'] = type.replace(' ', '_').lower()
    except ObjectDoesNotExist, e:
        log.info('Object Does Not Exist')
        log.error(e)
    except Exception, e:
        log.info('Unspecified Exception')
        log.error(e)
    return context

@register.inclusion_tag("generic/includes/tag_carousel.html", takes_context=True)
def content_carousel_for_tag(context, topic=None):
    gparent = BCCFPage.objects.get(slug='bccf/tag')
    
    filter = {
        'gparent': gparent,
        'status': 2,
        'publish_date__lte': datetime.datetime.now(),
        'featured': True
    }
    
    if topic:
        filter['topic'] = topic

    context['talks'] = BCCFChildPage.objects.filter(BCCF_EXPIRY, content_model='topic', **filter).order_by('-created')[:10]
    context['acts'] = BCCFChildPage.objects.filter(BCCF_EXPIRY, content_model='formpublished', **filter).order_by('-created')[:10]
    context['gets'] = BCCFChildPage.objects.filter(BCCF_EXPIRY, content_model='campaign', **filter).order_by('-created')[:10]
    return context

@register.inclusion_tag("generic/includes/resource_carousel.html", takes_context=True)
def content_carousel_for_resources(context, topic=None):
    filter = {
        'status': 2,
        'publish_date__lte': datetime.datetime.now(),
    }
    q_resources = Q(content_model='article') | Q(content_model='downloadableform') | Q(content_model='magazine') | Q(content_model='tipsheet') | Q(content_model='video')
    if topic:
        filter['topic'] = topic
    
    context['slides'] = BCCFChildPage.objects.filter(q_resources, BCCF_EXPIRY, **filter).order_by('-created')[:10]
    return context