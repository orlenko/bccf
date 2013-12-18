from django.db.models import get_model, ObjectDoesNotExist, Q
from mezzanine import template

import logging
import re

log = logging.getLogger(__name__)

register = template.Library()

@register.inclusion_tag("generic/includes/content_carousel.html", takes_context=True)
def content_carousel_for(context, obj, type=None):
    """
    Provides a generic context variable name for the object that carousels are
    being rendered for.
    """
    page = re.split('/get/', context['request'].path)
    params = None
    context['open'] = False

    if len(page) == 2:
        params = page[1].split('/') 
    
    context['filter'] = False
    if type == 'families' or type == 'professionals':
        if obj.title == 'Programs':
            pass
        elif obj.title == 'Events':
            pass
        else: # Topic
            pass
    else:
        try:
            if obj.title == 'Resources':
                model = get_model('bccf', type)
                context['slides'], context['open'] = content_helper(model, params, type)
                context['carouselTitle'] = type
                context['carouselID'] = "%s_id" % (type.replace(' ', '_').lower())
            elif obj.title == 'Tag':
                context['filter'] = True
            elif obj.title == 'News':
                model = get_model('news', 'NewsPost')
                context['slides'], context['open'] = content_helper(model, params, 'News')
                context['carouselTitle'] = 'News'
                context['carouselID'] = 'news'
            elif obj.title == 'Blog':
                from mezzanine.blog.models import BlogPost
                #model = get_model('Mezzanine.blog', 'BlogPost')
                context['slides'], context['open'] = content_helper(BlogPost, params, 'Blog')
                context['carouselTitle'] = 'Blog'
                context['carouselID'] = 'blog'
        except:
            return
    context['carouselColor'] = obj.carouselColor
    return context
    
def content_helper(model, params, type = None):
    try:
        if params is not None and type == params[1]:
            slides = [model.objects.get(slug=params[2])]
            slides.extend(model.objects.filter(~Q(slug=params[2])).order_by('-created')[:11])
            open = True
            return (slides, open)
        else:
            slides = model.objects.all().order_by('-created')[:12]
            return (slides, False)
    except ObjectDoesNotExist:
        log.error('Object Does not exist')
        return ([], False)
