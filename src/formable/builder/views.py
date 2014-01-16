import json
import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from django.shortcuts import redirect
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response

from formable.builder.models import FormStructure, FormPublished, Question, FieldAnswer, FormFilled
from formable.builder.forms import ViewFormForm, FormStructureForm
from formable.builder.utils import parse

from bccf.models import BCCFChildPage

log = logging.getLogger(__name__)
    
@require_http_methods(["POST"])
@login_required
@never_cache
def save_structure(request):
    """
    Saves a form structure to be cloned later. The any request that is not post
    will be redirected to the form builder. If all goes well, the user will be
    redirected to view the form as HTML.
    """
    form = FormStructureForm(request.POST, request.FILES)
    if form.is_valid():
        form_published = form.save(request.user)
        form.handle_upload()
    
    return redirect(form_published.get_absolute_url())
     
@require_http_methods(["POST"])
@login_required
@never_cache
def submit_form(request):
    """
    Submits a filled form. Every answer will its own separate row.
    """  
    try:
        publish_obj = FormPublished.objects.get(id=request.POST.get("publish_id"))
    except ObjectDoesNotExist:
        raise Http404
        
    form_filled = FormFilled(form_published=publish_obj, user=request.user)
    form_filled.save()
    
    for id in request.POST:
        key = id.split('.', 1)
        if key[0].isdigit():
            try:
                question_obj = Question.objects.get(pk=key[0])
            except ObjectDoesNotExist:
                raise Http404
            if key[1] == "checkbox_field" or key[1] == "multiselect_field": # Check if it's a multi-answer field
                answers = request.POST.getlist(id)
                for ans in answers:
                    answer = FieldAnswer(form_filled=form_filled, question=question_obj,
                        answer=ans)
                    answer.save()
            else: # not multi-answer field
                answer = FieldAnswer(form_filled=form_filled, question=question_obj,
                    answer=request.POST.get(id))
                answer.save()    
    
    return redirect('/formable/success')
    
@require_http_methods(["POST"])
@never_cache
def publish_form(request):
    """
    Publishes a form so that it can be filledo out by users. A published form
    will be based on a form structure that was previously created.
    
    When a form is published, the fields in the form structure will be stored in
    the Questions table referencing to the newly published form.
    """
    if request.user.is_authenticated():
        struct_id = request.POST.get('struct_id', '')
        try:
            if struct_id == '':
                raise ObjectDoesNotExist
                
            struct_obj = FormStructure.objects.get(id=struct_id)
        except ObjectDoesNotExist:
            return redirect('/');
            
        form_published = FormPublished(form_structure=struct_obj, user=request.user)
        form_published.save()

        # Create Questions based on structure
        struct = json.loads(struct_obj.structure)
        for fieldset in struct["fieldset"]:
            for field in fieldset["fields"]:
                if "label" in field: # don't save static text
                    if "required" in field["attr"]:
                        required = 1
                    else:
                        required = 0
                    
                    if "options" in field:
                        num_answers = len(field["options"])
                        
                    question = Question(question=field["label"], 
                        form_published=form_published, required=required,
                        num_answers=len(field["options"]) or '')
                    question.save()
        # End Create Questions
            
        return redirect('/formable/view/'+str(form_published.id))
    else:
        return redirect('/')
    
@require_http_methods(["GET"])
@login_required
@never_cache
def create_survey(request):
    structure_form = FormStructureForm()
    context = RequestContext(request, locals())
    return render_to_response('builder_page.html', {}, context_instance=context)

@login_required    
@never_cache
def clone_structure(request):
    pass
    
@require_http_methods(["GET"])
@login_required
@never_cache
def view(request, slug=None):
    """
    Creates a view based on the ID passed via GET. If there's no ID or not a GET, 
    it will redirect the user to the index page.
    """
    if slug == None:
        raise Http404
    #page = BCCFChildPage.objects.get(slug=slug)
    page = FormPublished.objects.get(slug=slug)
    form_structure = FormStructure.objects.get(pk=page.form_structure.pk)
    fieldset, field = parse(form_structure.structure, page.pk)
    form = ViewFormForm(fieldset, field)
    form_title = form_structure.title
    form = form
    publish_id =  page.pk
    context = RequestContext(request, locals())
    return render_to_response('view_form.html', {}, context_instance=context)

