from django.shortcuts import render_to_response, render
from django.template.context import RequestContext
from django.db.models import ObjectDoesNotExist
from django.http import HttpResponse
from django.core import serializers

from bccf.models import BCCFPage, BCCFChildPage, BCCFBabyPage, BCCFTopic

import logging
import json

log = logging.getLogger(__name__)

def page(request, parent, child=None, baby=None):
    if(not request.is_ajax()):
        page = BCCFPage.objects.get(slug=parent)
        template = 'bccf/%s_page.html' % (parent)
    else: 
        baby_obj = None
        if baby and baby != 'resources':
            baby_obj = BCCFBabyPage.objects.get(slug=('%s/%s') % (child, baby))
        elif baby == 'resources':
            baby_obj = 'resources'
        child_obj = BCCFChildPage.objects.get(slug=child)
        babies = (BCCFChildPage.objects.filter(parent=child_obj))
        template = 'generic/sub_page.html'
        log.info(baby_obj)
        #Related resources
    context = RequestContext(request, locals())
    return render_to_response(template, {}, context_instance=context)
    
def topic_page(request, topic):
    page = BCCFTopic.objects.get(slug=topic)
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