import json

from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import redirect
from django.views.decorators.cache import never_cache

from formable.builder.models import FormStructure
from formable.builder.forms import CloneFormForm, ViewFormForm
from formable.builder.utils import parse

@never_cache
def index(request):
    """
    Calls the index template. Creates a dropdown select containing all the created
    form structures for cloning.
    """
    template_name = 'index.html'
    form = CloneFormForm()
    clone_url = '/build/'
    template = loader.get_template(template_name)
    context = RequestContext(request, {
        'form': form,
        'clone_url': clone_url
    })
    
    return HttpResponse(template.render(context))
    
@never_cache
def build(request, id=None):
    """
    Calls the builder template. If the request is a post, it looks for the ID
    of an existing form structure to clone.
    """
    template_name = 'builder.html'
    template = loader.get_template(template_name)
    if request.method == 'GET':
        if id is not None:
            form_structure = FormStructure.objects.get(pk=id)
            context = RequestContext(request, {
                'form_structure': json.dumps(form_structure.form_structure)
            })
        else:
            context = RequestContext(request)
        
    return HttpResponse(template.render(context));
    
@never_cache
def save(request):
    """
    Saves a form structure to be cloned later. The any request that is not post
    will be redirected to the form builder. If all goes well, the user will be
    redirected to view the form as HTML.
    """
    if request.method == 'POST':
        form_structure = FormStructure.objects.create(
            form_title = request.POST.get('form_structure_title', ''),
            form_structure = request.POST.get('form_structure_data', ''),
            form_structure_type = request.POST.get('form_structure_type', ''),
        )
        return redirect('/view/'+str(form_structure.id))
    else:
        return redirect('/build/')
        
@never_cache
def delete(request):
    """
    Deletes the form structure
    """
    if request.method == 'POST':
        id = request.POST.get('form_structures', '')
        FormStructure.objects.filter(id=id).delete()
    
    return redirect('/')

@never_cache
def view(request, id=None):
    """
    Creates a view based on the ID passed via GET. If there's no ID or not a GET, 
    it will redirect the user to the index page.
    """
    if request.method == 'GET':
        template_name = 'view_form.html'
        template = loader.get_template(template_name)
        
        if id == None:
            return redirect('/')
        
        form_structure = FormStructure.objects.get(pk=id)
        struct = parse(form_structure.form_structure)
        form = ViewFormForm(struct[0], struct[1])
        context = RequestContext(request, {
            'form_title': form_structure.form_title,
            'form': form,
        })
        return HttpResponse(template.render(context))
    else:
        return redirect('/')
