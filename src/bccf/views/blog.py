import logging

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.db.models import ObjectDoesNotExist

from bccf.models import BCCFPage

log = logging.getLogger(__name__)

def blog_page(request, type=None):
    page = BCCFPage.objects.get(slug='blog')
    context = RequestContext(request, locals())
    return render_to_response('bccf/news_blog_page.html', {}, context_instance=context)