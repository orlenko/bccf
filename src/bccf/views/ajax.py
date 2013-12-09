import logging

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.db.models import get_model, ObjectDoesNotExist

log = logging.getLogger(__name__)

# File containing all views that are called via AJAX
def get(request, parent, type, page):
    log.info(parent)
    model = get_model('bccf', type)
    obj = model.objects.get(slug=page)
    context = RequestContext(request, locals())        
    return render_to_response('generic/%s_page_box.html' % (parent.lower()), {}, context_instance=context);