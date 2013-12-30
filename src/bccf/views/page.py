from django.shortcuts import render_to_response, render
from django.template.context import RequestContext
from django.db.models import ObjectDoesNotExist
from django.http import HttpResponse
from django.core import serializers
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404

from bccf.models import BCCFPage, BCCFChildPage, BCCFBabyPage, BCCFTopic

import logging
import json

log = logging.getLogger(__name__)

@staff_member_required
def bccf_admin_page_ordering(request):
    """
    Updates the ordering of pages via AJAX from within the admin.
    """

    def get_id(s):
        s = s.split("_")[-1]
        return s if s and s != "null" else None
    page = get_object_or_404(BCCFChildPage, id=get_id(request.POST['id']))
    old_parent_id = page.parent_id
    new_parent_id = get_id(request.POST['parent_id'])
    if new_parent_id != page.parent_id:
        # Parent changed - set the new parent and re-order the
        # previous siblings.
        if new_parent_id is not None:
            new_parent = BCCFChildPage.objects.get(id=new_parent_id)
        else:
            new_parent = None
        page.set_parent(new_parent)
        pages = BCCFChildPage.objects.filter(parent_id=old_parent_id)
        for i, page in enumerate(pages.order_by('_order')):
            BCCFChildPage.objects.filter(id=page.id).update(_order=i)
    # Set the new order for the moved page and its current siblings.
    for i, page_id in enumerate(request.POST.getlist('siblings[]')):
        BCCFChildPage.objects.filter(id=get_id(page_id)).update(_order=i)
    return HttpResponse("ok")

def page(request, parent, child=None, baby=None):
    if(not request.is_ajax()):
        page = get_object_or_404(BCCFPage, slug=parent)
        template = 'bccf/%s_page.html' % (parent)
    else: 
        baby_obj = None
        log.info('TEST')
        if baby and baby != 'resources':
            baby_obj = BCCFBabyPage.objects.get(slug=('%s/%s') % (child, baby))
        elif baby and baby == 'resources':
            baby_obj = 'resources'
        log.info('TEST 2')
        child_obj = BCCFChildPage.objects.get(slug=child)
        babies = BCCFChildPage.objects.filter(parent=child_obj).order_by('_order')
        template = 'generic/sub_page.html'
        log.info(baby_obj)
        #Related resources
    context = RequestContext(request, locals())
    return render_to_response(template, {}, context_instance=context)
    
def topic_page(request, topic):
    page = get_object_or_404(BCCFTopic, slug=topic)
    context = RequestContext(request, locals())
    return render_to_response('bccf/topic_page.html', {}, context_instance=context)
    
def next(request, parent, which, offset):
    obj = BCCFPage.objects.get(slug=parent)
    if obj.title == 'Reources' or obj.title == 'TAG':
        slides = BCCFChildPage.objects.filter(gparent=obj.pk, content_model=which).order_by('-created')[offset:12]
    elif which == 'parent' or which == 'professional':
        slides = BCCFChildPage.objects.filter(gparent=obj.pk, page_for=which).order_by('-created')[offset:12]
    else:
        slides = BCCFChildPage.objects.filter(gparent=obj.pk).order_by('-created')[offset:12]
    data = serializers.serialize('json', slides)
    return HttpResponse(json.dumps(data), content_type="application/json")   

def topic_next(request, topic, which, offset):
    topic = BCCFTopic.objects.get(slug=topic)    
    json_data = serializers.serialize('json', BCCFChildPage.objects.filter(topic=topic, page_for=which).order_by('-created')[offset:12])
    return HttpResponse(json.dumps(json_data), content_type="application/json")