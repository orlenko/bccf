from django.db.models import get_model, ObjectDoesNotExist, Q
from mezzanine import template
from mezzanine.pages.models import Page

from bccf.models import BCCFChildPage, BCCFPage

import logging
import re

log = logging.getLogger(__name__)

register = template.Library()

@register.inclusion_tag("generic/includes/content_carousel.html", takes_context=True)
def product_category_carousel(context, category):
    page = re.split('/get/', context['request'].path)
    params = None
    context['open'] = False
    context['filter'] = False
    context['carousel_color'] = category.get_content_model().carousel_color
    context['carousel_title'] = 'Products'
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

    if title == 'Talk':
        context['filter'] = True
    try:
        if child is None:
            if which is None:
                context['slides'] = BCCFChildPage.objects.filter(gparent=obj.pk, status=2).order_by('-created')[:12]
            else:
                if obj.slug == 'bccf/resources' or obj.slug == 'bccf/tag':
                    context['slides'] = BCCFChildPage.objects.filter(gparent=obj.pk, content_model=which, status=2).order_by('-created')[:12]
                else:
                    context['slides'] = BCCFChildPage.objects.filter(gparent=obj.pk, page_for=which, status=2).order_by('-created')[:12]
        elif which is None:
            context['open'] = True
            context['slides'] = [BCCFChildPage.objects.get(slug=child)]
            context['slides'].extend(BCCFChildPage.objects.filter(~Q(slug=child), gparent=obj.pk, status=2).order_by('-created')[:11])
        elif obj.slug == 'bccf/resources' or obj.slug == 'bccf/tag': #Multiple
            temp = BCCFChildPage.objects.get(slug=child)
            log.info('HERE')
            if temp.content_model == which: #For different content models
                context['open'] = True
                context['slides'] = [temp]
                context['slides'].extend(BCCFChildPage.objects.filter(~Q(slug=child), gparent=obj.pk, content_model=which, status=2).order_by('-created')[:11])
            else:
                context['slides'] = BCCFChildPage.objects.filter(gparent=obj.pk, content_model=which, status=2).order_by('-created')[:12]
        else:
            temp = BCCFChildPage.objects.get(slug=child)
            if temp.page_for == which: #For parent or professional
                context['open'] = True
                context['slides'] = [temp]
                context['slides'].extend(BCCFChildPage.objects.filter(~Q(slug=child), gparent=obj.pk, page_for=which, status=2).order_by('-created')[:11])
            else:
                context['slides'] = BCCFChildPage.objects.filter(gparent=obj.pk, page_for=which,status=2).order_by('-created')[:12]
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
    try:
        context['slides'] = BCCFChildPage.objects.filter(bccf_topic=topic, page_for=type, status=2).order_by('-created')[:12]
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
    if topic:
        context['talks'] = BCCFChildPage.objects.filter(gparent=gparent, content_model='topic', featured=True, bccf_topic=topic, status=2).order_by('-created')[:10]
        context['acts'] = BCCFChildPage.objects.filter(gparent=gparent, content_model='formpublished', featured=True, bccf_topic=topic, status=2).order_by('-created')[:10]
        context['gets'] = BCCFChildPage.objects.filter(gparent=gparent, content_model='campaign', featured=True, bccf_topic=topic, status=2).order_by('-created')[:10]
    else:
        context['talks'] = BCCFChildPage.objects.filter(gparent=gparent, content_model='topic', featured=True, status=2).order_by('-created')[:10]
        context['acts'] = BCCFChildPage.objects.filter(gparent=gparent, content_model='formpublished', featured=True, status=2).order_by('-created')[:10]
        context['gets'] = BCCFChildPage.objects.filter(gparent=gparent, content_model='campaign', featured=True, status=2).order_by('-created')[:10]
    return context

@register.inclusion_tag("generic/includes/resource_carousel.html", takes_context=True)
def content_carousel_for_resources(context, topic=None):
    if topic:
        context['slides'] = BCCFChildPage.objects.filter(Q(content_model='article', topic=topic) | Q(content_model='downloadableform', topic=topic) | Q(content_model='magazine', topic=topic) | Q(content_model='tipsheet', topic=topic) | Q(content_model='video', topic=topic), status=2).order_by('-created')
    else:
        context['slides'] = BCCFChildPage.objects.filter(Q(content_model='article') | Q(content_model='downloadableform') | Q(content_model='magazine') | Q(content_model='tipsheet') | Q(content_model='video'), status=2).order_by('-created')[:10]
    return context