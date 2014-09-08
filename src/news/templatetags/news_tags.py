import datetime
from django.template import Context
from django.template.loader import get_template
from mezzanine import template
import logging

from bccf.models import BCCFChildPage

log = logging.getLogger(__name__)

register = template.Library()

@register.render_tag
def news_list(context, token):
    context['news'] = BCCFChildPage.objects.filter(publish_date__lt=datetime.datetime.now(), content_model='newspost').order_by('-publish_date')[:3]
    t = get_template('news/news_widget.html')
    return t.render(Context(context))
