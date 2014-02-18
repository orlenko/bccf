import logging

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.decorators.cache import never_cache

from bccf.util.memberutil import require_event_audience
from bccf.models import Event, EventRegistration, BCCFPage
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from bccf.forms import EventForm
from django.http.response import HttpResponseRedirect
from mezzanine.core.models import CONTENT_STATUS_DRAFT, CONTENT_STATUS_CHOICES
from django import forms

log = logging.getLogger(__name__)



def event_page(request):
    page = BCCFPage.objects.get(slug='trainings')
    context = RequestContext(request, locals())
    return render_to_response('bccf/events_page.html', {}, context_instance=context)


@login_required
def create(request):
    page_for = request.user.profile.provided_event_type
    form = EventForm(initial={
        'provider': request.user,
        'page_for': page_for,
        'status': CONTENT_STATUS_DRAFT,
    })
    if request.method == 'POST':
        form = EventForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            if not form.instance.parent:
                try:
                    form.instance.parent = BCCFPage.objects.get(slug='trainings')
                    form.instance.save()
                except:
                    pass
            messages.success(request, 'Event created successfully.')
            return HttpResponseRedirect(form.instance.edit_url())
    context = RequestContext(request, locals())
    return render_to_response('bccf/event_create.html', {}, context_instance=context)


@login_required
def edit(request, slug):
    event = Event.objects.get(slug=slug)
    form = EventForm(instance=event)
    form.fields['status'].widget = forms.Select(choices=CONTENT_STATUS_CHOICES)
    if request.method == 'POST':
        form = EventForm(data=request.POST, files=request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully.')
            return HttpResponseRedirect(form.instance.get_absolute_url())
    context = RequestContext(request, locals())
    return render_to_response('bccf/event_update.html', {}, context_instance=context)


@require_event_audience
@never_cache
def signup(request, slug):
    if 'aftercheckout' in request.session:
        del request.session['aftercheckout']
    event = Event.objects.get(slug=slug)
    if request.method == 'POST':
        # Check if such registration already exists
        exists = False
        for existing in EventRegistration.objects.filter(user=request.user, event=Event.objects.get(slug=slug)):
            messages.warning(request, 'You are already signed up to this event')
            exists = True
        if not exists:
            registration = EventRegistration.objects.create(user=request.user, event=Event.objects.get(slug=slug))
            messages.success(request, 'Thank you! You signed up to the event successfully.')
        return HttpResponseRedirect(event.get_absolute_url())
    context = RequestContext(request, locals())
    return render_to_response('bccf/event_signup.html', {}, context_instance=context)


def event(request):
    pass