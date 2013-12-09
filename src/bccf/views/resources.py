import logging

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.db.models import ObjectDoesNotExist


from bccf.models import Page

log = logging.getLogger(__name__)

def resources_page(request, type=None):
    page = Page.objects.get(slug='resources')
    
    context = RequestContext(request, locals())
    return render_to_response('bccf/resource_page.html', {}, context_instance=context)