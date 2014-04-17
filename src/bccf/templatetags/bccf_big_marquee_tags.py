from django.db.models import ObjectDoesNotExist, Q
from mezzanine import template
from bccf.models import BCCFPage, BCCFChildPage, BCCFTopic, HomeMarquee, HomeMarqueeSlide, PageMarqueeSlide, Program

import logging
import datetime

log = logging.getLogger(__name__)

register = template.Library()

@register.inclusion_tag("generic/includes/big_marquee.html", takes_context=True)
def big_marquee_for(context, obj=None):
    """
    Provides generic content variable for the big marquee.
    """
    context['show_tag'] = False
    if not obj: # For index
        context['show_tag'] = True
        try:
            homeMarquee = HomeMarquee.objects.get(active=True)
            context['slides'] = HomeMarqueeSlide.objects.filter(marquee=homeMarquee)
        except ObjectDoesNotExist:
            pass
    else:
        context['marquee_class'] = 'page-marquee'
        context['slides'] = PageMarqueeSlide.objects.filter(marquee=obj.marquee)
    return context
    
@register.inclusion_tag("generic/includes/browse_by.html", takes_context=True)
def browse_by(context):
    context['programs']  = Program.objects.filter(user_added=0)
    context['topics'] = BCCFTopic.objects.all()
    return context