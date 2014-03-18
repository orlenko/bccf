from django.db.models import get_model, ObjectDoesNotExist, Q
from mezzanine import template
from mezzanine.pages.models import Page

from bccf.models import BCCFChildPage, BCCFPage, Campaign, Article
from formable.builder.models import FormPublished
from pybb.models import Topic

import logging
import re
import datetime

log = logging.getLogger(__name__)
register = template.Library()

@register.inclusion_tag("generic/includes/content_carousel.html", takes_context=True)
def product_category_carousel(context, category, product=None):
    page = re.split('/get/', context['request'].path)
    params = None
    context['open'] = False
    context['filter'] = False
    context['carousel_color'] = category.get_content_model().carousel_color
    context['carousel_title'] = category.title
    context['carousel_name'] = 'products'
    if product and product.categories.filter(slug=category.slug).exists():
        context['slides'] = [product]
        context['slides'].extend(category.get_content_model().products.filter(~Q(slug__exact=product.slug)))
    else:
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
    context['slides'] = []

    limit = 12

    slides = BCCFChildPage.objects.by_gparent(obj)

    if title == 'Talk':
        context['filter'] = True
    try:
        if which:
            if obj.slug == 'bccf/resources' or obj.slug == 'bccf/tag':
                slides = slides.filter(content_model=which)
            else:
                slides = slides.filter(page_for=which)
        if child:
            temp = slides.filter(slug=child)
            context['open'] = True
            context['slides'].extend(temp)
            slides = slides.filter(~Q(slug=child))
            limit = 11
            
        context['slides'].extend(slides.order_by('-created')[:limit])
            
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
        context['slides'] = BCCFChildPage.objects.by_topic(topic).filter(page_for=type).order_by('-created')[:12]
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
def content_carousel_for_tag(context):
    context['talks'] = Topic.objects.talks().filter(featured=True).order_by('-created')[:10]
    context['acts'] = FormPublished.objects.acts().filter(featured=True).order_by('-created')[:10]
    context['gets'] = Campaign.objects.gets().filter(featured=True).order_by('-created')[:10]
    return context

@register.inclusion_tag("generic/includes/resource_carousel.html", takes_context=True)
def content_carousel_for_resources(context):
    context['slides'] = BCCFChildPage.objects.published().filter(Q(content_model='article') | Q(content_model='downloadableform') | Q(content_model='magazine') | Q(content_model='podcast') | Q(content_model='tipsheet') | Q(content_model='video')).order_by('-created')[:10]
    return context