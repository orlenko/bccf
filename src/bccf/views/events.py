import logging
import csv
import datetime

from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template.context import RequestContext
from django.views.decorators.cache import never_cache
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django import forms

from cartridge.shop.models import ProductVariation
from cartridge.shop.utils import recalculate_cart

from bccf.util.memberutil import require_event_audience
from bccf.util.emailutil import send_moderate, send_reminder
from bccf.models import Event, EventRegistration, BCCFPage
from bccf.forms import EventForm
from mezzanine.core.models import CONTENT_STATUS_DRAFT, CONTENT_STATUS_PUBLISHED, CONTENT_STATUS_CHOICES

log = logging.getLogger(__name__)

def event_page(request):
    page = BCCFPage.objects.get(slug='trainings')
    context = RequestContext(request, locals())
    return render_to_response('bccf/events_page.html', {}, context_instance=context)


@login_required
def create(request):
    form = EventForm(request.user, initial={
        'provider': request.user,
        'page_for': 'parent',
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

@login_required
def publish(request, slug):
    event = Event.objects.get(slug=slug)
    event.status = CONTENT_STATUS_PUBLISHED
    event.save()
    send_moderate("An Event has been published", context={'event':event})
    messages.success(request, 'Event published. The event will be subject to review and can be taken down without notice.')
    return redirect(reverse('update-tab', (), {'tab': 'training'}))

#@require_event_audience
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
               if event.event_product:
                   variation = ProductVariation.objects.get(sku='EVENT-%s' % event.pk)
                   request.cart.add_item(variation, 1)
                   recalculate_cart(request)
                   messages.success(request, 'To complete the registration, please go through the checkout.')
                   
                   # Send event registration confirmation
                   send_reminder("Event Registration Pending.", request.user, context={'event':event})
                   
               else:
                   registration = EventRegistration.objects.create(user=request.user, event=event)
                   
                   # Send event registration confirmation
                   send_reminder("Event Registration Complete.", request.user, context={'event':event})
                   
                   messages.success(request, 'Thank you! You signed up to the event successfully.')              
           if event.max_seats == len(EventRegistration.objects.filter(event=event)):
               event.full = True
               event.save()

               # Send event registration for provider
               attendees = EventRegistration.objects.filter(event=event)
               send_reminder("Event is now full", event.provider, context={'event':event, 'attendees':attendees})
             
           # Send event registration for provider
           send_reminder("A user registered for your event", event.provider, context={'event':event, 'attendee':request.user})
             
        else:
            messages.warning(request, 'The event is full.')
            
        return HttpResponseRedirect(event.get_absolute_url())
    context = RequestContext(request, locals())
    return render_to_response('bccf/event_signup.html', {}, context_instance=context)

def event_payment(request, event_id):
    user = request.user
    event_reg = get_object_or_404(EventRegistration, event=event_id, user=user, ~Q(paid=True))
    event = event_reg.event
    variation = ProductVariation.objects.get(sku='EVENT-%s' % event.pk)
    request.cart.add_item(variation, 1)
    recalculate_cart(request)
    return redirect('shop/checkout')

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
    