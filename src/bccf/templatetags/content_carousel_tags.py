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
        pass
    else:
        if obj.title == 'Resources':
            model = get_model('bccf', type)
            try:
                if params is not None and type == params[1]:
                    context['slides'] = [model.objects.get(slug=params[2])]
                    context['slides'].extend(model.objects.filter(~Q(slug=params[2])))
                    context['open'] = True
                else:
                    context['slides'] = model.objects.all()[:12]
            except ObjectDoesNotExist:
                log.error('Object Does not exist')
                return
            context['carouselTitle'] = type
            context['carouselID'] = "%s_id" % (type.replace(' ', '_').lower())
        elif obj.title == 'Tag':
            context['filter'] = True
        elif obj.title == 'News':
            pass
        elif obj.title == 'Blog':
            pass
    context['carouselColor'] = obj.carouselColor
    return context
