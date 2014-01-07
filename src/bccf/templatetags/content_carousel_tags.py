from django.db.models import get_model, ObjectDoesNotExist, Q
from mezzanine import template
from mezzanine.pages.models import Page

from bccf.models import BCCFChildPage, BCCFPage

import logging
import re

log = logging.getLogger(__name__)

register = template.Library()

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
    context['carousel_color'] = obj.carousel_color
    context['carousel_title'] = title
    context['carousel_name'] = which
    context['slides'] = None    
    
    if title == 'Talk':
        context['filter'] = True    
    
    try:
        if child is None:
            if which is None:
                context['slides'] = BCCFChildPage.objects.filter(gparent=obj.pk).order_by('-created')[:12]
            else:
                if obj.title == 'Resources' or obj.title == 'TAG':
                    context['slides'] = BCCFChildPage.objects.filter(gparent=obj.pk, content_model=which).order_by('-created')[:12]
                else:
                    context['slides'] = BCCFChildPage.objects.filter(gparent=obj.pk, page_for=which).order_by('-created')[:12]
        elif which is None:
            context['open'] = True
            context['slides'] = [BCCFChildPage.objects.get(slug=child)]
            context['slides'].extend(BCCFChildPage.objects.filter(~Q(slug=child), gparent=obj.pk).order_by('-created')[:11])
        elif obj.title == 'Resources' or obj.title == 'TAG': #Multiple
            temp = BCCFChildPage.objects.get(slug=child)
            if temp.content_model == which: #For different content models
                context['open'] = True
                context['slides'] = [temp]
                context['slides'].extend(BCCFChildPage.objects.filter(~Q(slug=child), gparent=obj.pk, content_model=which).order_by('-created')[:11])
            else:
                context['slides'] = BCCFChildPage.objects.filter(gparent=obj.pk, content_model=which).order_by('-created')[:12]
        else:
            temp = BCCFChildPage.objects.get(slug=child)
            if temp.page_for == which: #For parent or professional
                context['open'] = True
                context['slides'] = [temp]
                context['slides'].extend(BCCFChildPage.objects.filter(~Q(slug=child), gparent=obj.pk, page_for=which).order_by('-created')[:11])
            else:
                context['slides'] = BCCFChildPage.objects.filter(gparent=obj.pk, page_for=which).order_by('-created')[:12]   
    except ObjectDoesNotExist, e:
        log.info('Object Does Not Exist')
        log.error(e)
    except Exception, e:
        log.info('Unspecified Exception')
        log.error(e)
        return
    return context

@register.inclusion_tag("generic/includes/topic_carousel.html", takes_context=True)
def content_carousel_for_topic(context, topic, type):
    """
    The same a the content carousel_for but this focuses on all pages that are related to a Topic
    """
    try:
        context['slides'] = BCCFChildPage.objects.filter(bccf_topic=topic, page_for=type).order_by('-created')[:12]
        log.info(context['slides'])
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
    gparent = BCCFPage.objects.get(slug='tag')
    if topic:
        context['talks'] = BCCFChildPage.objects.filter(gparent=gparent, content_model='topic', bccf_topic=topic).order_by('-created')[:10]
        context['acts'] = BCCFChildPage.objects.filter(gparent=gparent, content_model='formpublished', bccf_topic=topic).order_by('-created')[:10]
        context['gets'] = BCCFChildPage.objects.filter(gparent=gparent, content_model='campaign', bccf_topic=topic).order_by('-created')[:10]
    else:
        context['talks'] = BCCFChildPage.objects.filter(gparent=gparent, content_model='topic').order_by('-created')[:10]
        context['acts'] = BCCFChildPage.objects.filter(gparent=gparent, content_model='formpublished').order_by('-created')[:10]
        context['gets'] = BCCFChildPage.objects.filter(gparent=gparent, content_model='campaign').order_by('-created')[:10]
    return context
    
@register.inclusion_tag("generic/includes/resource_carousel.html", takes_context=True)
def content_carousel_for_resources(context, topic=None):
    if topic:
        context['slides'] = BCCFChildPage.objects.filter(Q(content_model='article', topic=topic) | Q(content_model='downloadableform', topic=topic) | Q(content_model='magazine', topic=topic) | Q(content_model='tipsheet', topic=topic) | Q(content_model='video', topic=topic)).order_by('-created')
    else:
        context['slides'] = BCCFChildPage.objects.filter(Q(content_model='article') | Q(content_model='downloadableform') | Q(content_model='magazine') | Q(content_model='tipsheet') | Q(content_model='video')).order_by('-created')[:10]
    return context