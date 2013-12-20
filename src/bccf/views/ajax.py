import logging

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.db.models import get_model, ObjectDoesNotExist

log = logging.getLogger(__name__)

# File containing all views that are called via AJAX
def get(request, parent, type, page):
    log.info(parent)
    log.info(type)
    log.info(page)
    try:
        if parent == 'News' or parent == 'Blog':
            model = get_model(parent.lower(), '%sPost' % (parent))
            obj = model.objects.get(slug=page)
            context = RequestContext(request, locals())
            return render_to_response('generic/sub_page_box.html', {}, context_instance=context);
        elif parent == 'Programs/Professionals' or parent == 'Programs/Parents':
            model = get_model('bccf', 'Program')
            childModel = get_model('bccf', 'ProgramChild')
            obj = model.objects.get(slug='%s/%s' % (type, page))
            children = childModel.objects.filter(parent=obj)
            context = RequestContext(request, locals())
            return render_to_response('generic/programs_page_box.html', {}, context_instance=context);
        else:
            model = get_model('bccf', type)
        obj = model.objects.get(slug=page)
    except ObjectDoesNotExist, e:
        log.info('Object Does Not Exist')
        log.error(e)
    context = RequestContext(request, locals())
    return render_to_response('generic/%s_page_box.html' % (parent.lower()), {}, context_instance=context);
    
def add(request, offset, model):
    log.info(offset);
    return 'test';