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
from formable.builder.forms import ViewFormForm, FormStructureForm, CloneFormForm, FormPublishForm
from formable.builder.utils import parse
from bccf.models import Event
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse

log = logging.getLogger(__name__)


@login_required
@never_cache
def publish_form(request, id):
    """
    Publishes a form so that it can be filled out by users. A published form
    will be based on a form structure that was previously created.

    When a form is published, the fields in the form structure will be stored in
    the Questions table referencing to the newly published form.
    """
    try:
        if not request.user.is_superuser:
            struct = FormStructure.objects.get(user=request.user, pk=id)
        else:
            struct = FormStructure.objects.get(pk=id)
    except ObjectDoesNotExist:
        return redirect('/');

    if request.method == 'POST':
        form = FormPublishForm(request.POST)
        if form.is_valid():
            published = form.save(struct, request.user)

            # Support editing for events
            redirect_to_event = False
            if 'before_event' in request.GET:
                event = Event.objects.get(pk=int(request.GET['before_event']))
                log.debug('Updating event: %s' % event)
                event.survey_before_id = published.pk
                log.debug('Updated survey of %s: %s' % (event, event.survey_before_id))
                event.save()
                redirect_to_event = event
            if 'after_event' in request.GET:
                event = Event.objects.get(pk=int(request.GET['after_event']))
                log.debug('Updating event: %s' % event)
                event.survey_after_id = published.pk
                log.debug('Updated survey of %s: %s' % (event, event.survey_after_id))
                event.save()
                redirect_to_event = event
            if redirect_to_event:
                return HttpResponseRedirect(event.edit_url())

            return redirect(published.get_absolute_url())
    else:
        form = FormPublishForm()
        context = RequestContext(request, locals())
        return render_to_response('publish_form.html', {}, context_instance=context)


@login_required
@never_cache
def create_survey(request, type=None, id=None):
    """
    View to create a survey structure.
    """
    if request.method == 'POST':
        log.debug('Saving survey: %s - %s' % (request.POST, request.GET))
        form = FormStructureForm(request.POST)
        structure = request.POST['structure']
        if form.is_valid():
            if type == 'edit' and id:
                struct = FormStructure.objects.get(pk=id)
                struct.structure = request.POST['structure']
                struct.title = request.POST['title']
            else:
                struct = form.save(commit=False)
                if not request.user.is_superuser:
                    struct.user = request.user
            struct.save()

            # Support editing for events
            if 'before_event' in request.GET:
                log.debug('Before event: %s' % request.GET['before_event'])
                log.debug('Redirecting to publishing the form')
                return HttpResponseRedirect('%s?before_event=%s'
                    % (reverse('formable-publish-form', kwargs={'id': struct.pk}),
                       request.GET['before_event']))
            if 'after_event' in request.GET:
                log.debug('After event: %s' % request.GET['after_event'])
                log.debug('Redirecting to publishing the form')
                return HttpResponseRedirect('%s?after_event=%s'
                    % (reverse('formable-publish-form', kwargs={'id': struct.pk}),
                       request.GET['after_event']))

            context = RequestContext(request, locals())
            return render_to_response('success/create_struct.html', {}, context_instance=context)
    else:
        if id:
            struct = FormStructure.objects.get(pk=id)
            if not request.user.is_superuser and type == 'edit':
                if not struct.user or  struct.user != request.user:
                    return redirect('/')
            form = FormStructureForm(initial={'title':struct.title})
        else:
            form = FormStructureForm()
    if 'before_event' in request.REQUEST:
        before_event = request.REQUEST['before_event']
    if 'after_event' in request.REQUEST:
        after_event = request.REQUEST['after_event']
    context = RequestContext(request, locals())
    return render_to_response('builder_page.html', {}, context_instance=context)


@login_required
@never_cache
def view(request, slug=None):
    """
    Creates a view based on the ID passed via GET. If there's no ID or not a GET,
    it will redirect the user to the index page.
    """
    page = FormPublished.objects.get(slug=slug)
    filled = FormFilled.objects.filter(form_published=page, user=request.user)
    form_structure = FormStructure.objects.get(pk=page.form_structure.pk)
    fieldset, field = parse(form_structure.structure, page.pk)

    if len(filled) != 0:
        context = RequestContext(request, locals())
        return render_to_response('already_filled.html', {}, context_instance=context)

    if request.method == 'POST':
        form = ViewFormForm(fieldset, field, request.POST)

        if form.is_valid():
            template = 'success/submit_form.html'
            form_filled = FormFilled(form_published=page, user=request.user)
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
    else:
        template = 'view_form.html'
        form = ViewFormForm(fieldset, field)

    context = RequestContext(request, locals())
    return render_to_response(template, {}, context_instance=context)

