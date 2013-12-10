import logging

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.db.models import get_model, ObjectDoesNotExist

log = logging.getLogger(__name__)

# File containing all views that are called via AJAX
def get(request, parent, type, page):
    log.info(parent)
    log.info(type)
    if parent == 'News':
        model = get_model('news', 'NewsPost')
        obj = model.objects.get(slug=page)
        context = RequestContext(request, locals())
        return render_to_response('generic/sub_page_box.html', {}, context_instance=context);
    elif parent == 'Blog':
        from mezzanine.blog.models import BlogPost
        obj = BlogPost.objects.get(slug=page)
        context = RequestContext(request, locals())
        return render_to_response('generic/sub_page_box.html', {}, context_instance=context);
    else:
        model = get_model('bccf', type)
    obj = model.objects.get(slug=page)
    context = RequestContext(request, locals())
    return render_to_response('generic/%s_page_box.html' % (parent.lower()), {}, context_instance=context);
    
def add(request, offset, model):
    log.info(offset);
    return 'test';