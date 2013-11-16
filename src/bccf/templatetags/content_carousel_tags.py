from mezzanine import template

import logging

log = logging.getLogger(__name__)

register = template.Library()

@register.inclusion_tag("generic/includes/content_carousel.html", takes_context=True)
def content_carousel_for(context, obj=None):
    """
    Provides a generic context variable name for the object that carousels are
    being rendered for.
    """
    for s in ("slide1", "slide2", "slide3"):
        context["slide_" + s] = s
    return context
