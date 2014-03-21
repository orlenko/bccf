import logging
import csv
import datetime

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.decorators.cache import never_cache

from bccf.util.memberutil import require_event_audience
from bccf.models import Event, EventRegistration, BCCFPage
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from bccf.forms import EventForm
from django.http import HttpResponse
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
    form = EventForm(request.user, initial={
        'provider': request.user,
        'page_for': page_for,
        'status': CONTENT_STATUS_DRAFT,
    })
    if request.method == 'POST':
        form = EventForm(request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            if not form.instance.parent:
                try:
                    form.instance.gparent = BCCFPage.objects.get(slug='bccf/trainings')
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
        if not event.is_full():
            for existing in EventRegistration.objects.filter(user=request.user, event=event):
                messages.warning(request, 'You are already signed up to this event')
                exists = True
            if not exists:
                registration = EventRegistration.objects.create(user=request.user, event=event)
                messages.success(request, 'Thank you! You signed up to the event successfully.')                
            if event.max_seats == len(EventRegistration.objects.filter(event=event)):
                event.full = True
                event.save()
        else:
            messages.warning(request, 'The event is already full.')
            
        return HttpResponseRedirect(event.get_absolute_url())
    context = RequestContext(request, locals())
    return render_to_response('bccf/event_signup.html', {}, context_instance=context)


def event(request):
    pass
    
def attendees(request, id):
    event = Event.objects.get(id=id)
    if not request.user.is_authenticated() and not request.user.is_superuser() and event.user != request.user:
        redirect('/')
    
    attendees = EventRegistration.objects.filter(event=event)    
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s-%s-attendees.csv"' % (event.slug, datetime.datetime.now())
    
    writer = csv.writer(response)
    writer.writerow(['Attendees for %s' % (event.title)])
      
    writer.writerow(['First Name', 'Last Name', 'Email'])

    for attendee in attendees:
        writer.writerow([attendee.user.first_name, attendee.user.last_name, attendee.user.email])
    
    return response
    
def remove_survey(request):
    if request.is_ajax():
        event = None
        before = None
        if 'e' in request.GET:
            event = Event.objects.get(id=request.GET['e'])
        
        if 'b' in request.GET:
            before = True
        elif 'a' in request.GET:
            before = False
        
        if not event or not before:
            return HttpResponse('No')
            
        if before:
            before = event.survey_before
            event.survey_before = None
            event.save()
            before.delete()
        else:
            after = event.survey_after
            event.survey_after = None
            event.save()
            after.delete()
        return HttpResponse('Yes')
    else:
        return HttpResponse('No')
    