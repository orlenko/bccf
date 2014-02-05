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
from mezzanine.core.models import CONTENT_STATUS_DRAFT

log = logging.getLogger(__name__)



##################
# Generic Stuff
def event_page(request):
    page = BCCFPage.objects.get(slug='trainings')
    context = RequestContext(request, locals())
    return render_to_response('bccf/events_page.html', {}, context_instance=context)


# ##################
# # Parent Stuff
#
# def parents_event(request, slug):
#     try:
#         event = EventForParents.objects.get(slug=slug)  # @UndefinedVariable get
#     except ObjectDoesNotExist:
#         raise Http404
#     context = RequestContext(request, locals())
#     return render_to_response('bccf/event.html', {}, context_instance=context)
#
#
# @require_parent
# @never_cache
# def parents_event_signup(request, slug):
#     event = EventForParents.objects.get(slug=slug)
#     # Since we might have arrived through a membership-purchase page, let's clear the session variable that brought us here.
#     if 'aftercheckout' in request.session:
#         del request.session['aftercheckout']
#     context = RequestContext(request, locals())
#     return render_to_response('bccf/event_signup.html', {}, context_instance=context)

#
# #####################
# # Professional Stuff
#
# def professionals_event(request, slug):
#     try:
#         event = EventForProfessionals.objects.get(slug=slug)  # @UndefinedVariable get
#     except ObjectDoesNotExist:
#         raise Http404
#     context = RequestContext(request, locals())
#     return render_to_response('bccf/event.html', {}, context_instance=context)
#
#
# @require_professional
# @never_cache
# def professionals_event_signup(request, slug):
#     event = EventForProfessionals.objects.get(slug=slug)
#     # Since we might have arrived through a membership-purchase page, let's clear the session variable that brought us here.
#     if 'aftercheckout' in request.session:
#         del request.session['aftercheckout']
#     context = RequestContext(request, locals())
#     return render_to_response('bccf/event_signup.html', {}, context_instance=context)
#
#
# # For Professional Event Wizard
# FORMS = [('0', ProfessionalEventForm), # Main Form
#          ('1', FormStructureSurveyFormOne), # Before Survey
#          ('2', FormStructureSurveyFormTwo)]
#
# # Custom templates for each step
# TEMPLATES = {'0': 'bccf/wizard_event_create.html',
#              '1': 'generic/includes/form_builder.html',
#              '2': 'generic/includes/form_builder.html'}
#
#
# class ParentEventWizard(SessionWizardView):
#     """
#     Form Wizard for creating a new parent event
#
#     Steps: Event Details -> Before Survey (Optional) -> After Survey (Optional)
#     """
#     file_storage = FileSystemStorage(location=settings.MEDIA_ROOT+'/uploads/temp')
#
#     def get_template_names(self):
#         """
#         Override of form wizard's `get_template_names`
#
#         Returns the proper template depending on step
#         """
#         return [TEMPLATES[self.steps.current]]
#
#     def process_step(self, form):
#         """
#         Override of form wizard's `process_step`
#
#         Process a step when a form is submitted. The values in the form are clean and valid
#         """
#         if self.steps.current == '0': # Event form?
#             if '0-survey' in form.data and len(self.form_list) == 1: # Put back the deleted surveys if deleted before
#                 self.form_list['1'] = FORMS['1']
#                 self.form_list['2'] = FORMS['2']
#             elif '0-survey' not in form.data and len(self.form_list) == 3: # No Surveys delete the survey forms
#                 del self.form_list['1']
#                 del self.form_list['2']
#         elif self.steps.current == '1': # Before Survey form?
#             if '1-after_survey' in form.data and len(self.form_list) == 2: # After survey
#                 self.form_list['2'] = FORMS['2']
#             elif '1-after_survey' not in form.data and len(self.form_list) == 3: # No After Survey
#                 del self.form_list['2']
#         return self.get_form_step_data(form)
#
#     def get_context_data(self, form, **kwargs):
#         """
#         Override of form wizard's `get_context_data`
#
#         Adds form_structure to context for cloning before survey
#         """
#         context = super(ParentEventWizard, self).get_context_data(form=form, **kwargs)
#         if self.steps.current == '1': # Rebuild the form just in case the user goes back a step
#             before_data = self.get_cleaned_data_for_step(step=self.steps.current)
#             if before_data is not None and 'structure' in before_data:
#                 context.update({'form_structure':before_data['structure']})
#         elif self.steps.current == '2':
#             before_data = self.get_cleaned_data_for_step(step='1')
#             after_data = self.get_cleaned_data_for_step(step='2')
#             if before_data['clone']: # Clone the before form?
#                 context.update({'form_structure':before_data['structure']})
#             elif after_data is not None and 'structure' in after_data: # Rebuild the form just in case there's an error
#                 context.update({'form_structure':after_data['structure']})
#         return context
#
#     def done(self, form_list, **kwargs):
#         """
#         This is where the forms will be saved! If there are surveys, associate
#         them with the Event. Form structures will be automatically published.
#
#         REQUIRED by form wizard
#         """
#         event = form_list[0].save()
#         self.file_storage.delete(form_list[0].files['0-image'].name)
#         if len(form_list) >= 2: # If there's a before survey
#             event.survey_before = form_list[1].save(self.request.user)
#             event.survey_before.gparent = None
#             event.survey_before.parent = None
#             event.survey_before.save()
#         if len(form_list) == 3: # If there's an after survey
#             event.survey_after = form_list[2].save(self.request.user)
#             event.survey_after.gparent = None
#             event.survey_after.parent = None
#             event.survey_after.save()
#
#         event.save()
#         return redirect(event.get_absolute_url())
#
# class ProfessionalEventWizard(SessionWizardView):
#     """
#     Form Wizard for creating a new professional event
#
#     Steps: Event Details -> Before Survey (Optional) -> After Survey (Optional)
#     """
#     file_storage = FileSystemStorage(location=settings.MEDIA_ROOT+'/uploads/temp')
#
#     def get_template_names(self):
#         """
#         Override of form wizard's `get_template_names`
#
#         Returns the proper template depending on step
#         """
#         return [TEMPLATES[self.steps.current]]
#
#     def process_step(self, form):
#         """
#         Override of form wizard's `process_step`
#
#         Process a step when a form is submitted. The values in the form are clean and valid
#         """
#         if self.steps.current == '0': # Event form?
#             if '0-survey' in form.data and len(self.form_list) == 1: # Put back the deleted surveys if deleted before
#                 self.form_list['1'] = FORMS['1']
#                 self.form_list['2'] = FORMS['2']
#             elif '0-survey' not in form.data and len(self.form_list) == 3: # No Surveys delete the survey forms
#                 del self.form_list['1']
#                 del self.form_list['2']
#         elif self.steps.current == '1': # Before Survey form?
#             if '1-after_survey' in form.data and len(self.form_list) == 2: # After survey
#                 self.form_list['2'] = FORMS['2']
#             elif '1-after_survey' not in form.data and len(self.form_list) == 3: # No After Survey
#                 del self.form_list['2']
#         return self.get_form_step_data(form)
#
#     def get_context_data(self, form, **kwargs):
#         """
#         Override of form wizard's `get_context_data`
#
#         Adds form_structure to context for cloning before survey
#         """
#         context = super(ProfessionalEventWizard, self).get_context_data(form=form, **kwargs)
#         if self.steps.current == '1': # Rebuild the form just in case the user goes back a step
#             before_data = self.get_cleaned_data_for_step(step=self.steps.current)
#             if before_data is not None and 'structure' in before_data:
#                 context.update({'form_structure':before_data['structure']})
#         elif self.steps.current == '2':
#             before_data = self.get_cleaned_data_for_step(step='1')
#             after_data = self.get_cleaned_data_for_step(step='2')
#             if before_data['clone']: # Clone the before form?
#                 context.update({'form_structure':before_data['structure']})
#             elif after_data is not None and 'structure' in after_data: # Rebuild the form just in case there's an error
#                 context.update({'form_structure':after_data['structure']})
#         return context
#
#     def done(self, form_list, **kwargs):
#         """
#         This is where the forms will be saved! If there are surveys, associate
#         them with the Event. Form structures will be automatically published.
#
#         REQUIRED by form wizard
#         """
#         event = form_list[0].save()
#         self.file_storage.delete(form_list[0].files['0-image'].name)
#         if len(form_list) >= 2: # If there's a before survey
#             event.survey_before = form_list[1].save(self.request.user)
#             event.survey_before.gparent = None
#             event.survey_before.parent = None
#             event.survey_before.save()
#         if len(form_list) == 3: # If there's an after survey
#             event.survey_after = form_list[2].save(self.request.user)
#             event.survey_after.gparent = None
#             event.survey_after.parent = None
#             event.survey_after.save()
#
#         event.save()
#         return redirect(event.get_absolute_url())


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
            return HttpResponseRedirect(form.instance.get_absolute_url())
    context = RequestContext(request, locals())
    return render_to_response('bccf/event_create.html', {}, context_instance=context)


@require_event_audience
@never_cache
def signup(request, slug):
    if 'aftercheckout' in request.session:
        del request.session['aftercheckout']
    if request.method == 'POST':
        # Check if such registration already exists
        exists = False
        for existing in EventRegistration.objects.filter(user=request.user, event=Event.objects.get(slug=slug)):
            messages.warning(request, 'You are already signed up to this event')
            exists = True
        if not exists:
            registration = EventRegistration.objects.create(user=request.user, event=Event.objects.get(slug=slug))
            messages.success(request, 'Thank you! You signed up to the event successfully.')
    context = RequestContext(request, locals())
    return render_to_response('bccf/event_signup.html', {}, context_instance=context)


def event(request):
    pass