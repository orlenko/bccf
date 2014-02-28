from django.db.models import ObjectDoesNotExist, Q
from mezzanine import template
from bccf.models import BCCFPage, BCCFChildPage, BCCFTopic, HomeMarquee, HomeMarqueeSlide, PageMarqueeSlide, Program

import logging
import datetime

log = logging.getLogger(__name__)

register = template.Library()

BCCF_EXPIRY = Q(expiry_date__gte=datetime.datetime.now()) | Q(expiry_date=None)
BCCF_FILTER = {
    'status': 2,
    'publish_date__lte': datetime.datetime.now(),
}

@register.inclusion_tag("generic/includes/big_marquee.html", takes_context=True)
def big_marquee_for(context, obj=None):
    """
    Provides generic content variable for the big marquee.
    """
    context['slides'] = []
    context['show_tag'] = False
    if obj is None: # For index
        context['show_tag'] = True
        try:
            homeMarquee = HomeMarquee.objects.get(active=True)
            context['slides'] = HomeMarqueeSlide.objects.filter(marquee=homeMarquee)
        except ObjectDoesNotExist:
            pass
    elif obj.__class__.__name__ == 'BCCFTopic':
        if obj.marquee:
            try:
                context['slides'] = PageMarqueeSlide.objects.filter(marquee=obj.marquee)
            except ObjectDoesNotExist:
                pass
    else: # For other pages
        if obj.get_content_model().marquee:
            try:
                context['slides'] = PageMarqueeSlide.objects.filter(marquee=obj.get_content_model().marquee)
            except ObjectDoesNotExist:
                pass
    return context
    
@register.inclusion_tag("generic/includes/browse_by.html", takes_context=True)
def browse_by(context):
    context['programs']  = Program.objects.filter(BCCF_EXPIRY, user_added=0, **BCCF_FILTER)
    context['topics'] = BCCFTopic.objects.filter(BCCF_EXPIRY, **BCCF_FILTER)
    return context