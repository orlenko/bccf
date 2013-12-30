from django.db.models import ObjectDoesNotExist
from mezzanine import template
from bccf.models import BCCFPage, BCCFChildPage, BCCFTopic, HomeMarquee, HomeMarqueeSlide, PageMarqueeSlide

import logging

log = logging.getLogger(__name__)

register = template.Library()

@register.inclusion_tag("generic/includes/big_marquee.html", takes_context=True)
def big_marquee_for(context, obj=None):
    """
    Provides generic content variable for the big marquee.
    """
    page = BCCFPage.objects.get(slug='programs')
    context['programs']  = BCCFChildPage.objects.filter(gparent=page)
    context['topics'] = BCCFTopic.objects.all()
    if obj is None: # For index
        context['show_tag'] = True
        try:
            homeMarquee = HomeMarquee.objects.get(active=True)
            context['slides'] = HomeMarqueeSlide.objects.filter(marquee=homeMarquee)
        except ObjectDoesNotExist:
            pass
    else: # For other pages
        context['show_tag'] = False
        if obj.marquee:
            try:
                context['slides'] = PageMarqueeSlide.objects.filter(marquee=obj.marquee)
            except ObjectDoesNotExist:
                pass
    return context