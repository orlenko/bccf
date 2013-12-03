from mezzanine import template

import logging

log = logging.getLogger(__name__)

register = template.Library()

@register.inclusion_tag("generic/includes/content_carousel.html", takes_context=True)
def content_carousel_for(context, obj=None, type=None):
    """
    Provides a generic context variable name for the object that carousels are
    being rendered for.
    """
    if type == 'professionals':
        pass
    elif type == 'families':
        pass   
    return context
