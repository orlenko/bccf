import logging

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.db.models import ObjectDoesNotExist


from bccf.models import BCCFPage

log = logging.getLogger(__name__)

def programs_page(request, type=None):
    page = BCCFPage.objects.get(slug='programs')
    
    context = RequestContext(request, locals())
    return render_to_response('bccf/bccf_page.html', {}, context_instance=context)