import logging
import json
import csv
import time

from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from django.contrib.formtools.wizard.views import SessionWizardView
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse

from bccf.models import EventForParents, EventForProfessionals
from bccf.util.membership import require_parent, require_professional
from bccf.forms import ProfessionalEventForm, ParentEventForm, FormStructureSurveyFormOne, FormStructureSurveyFormTwo, ProfessionalSurveyReport
from django.views.decorators.cache import never_cache

from formable.builder.models import FormStructure, FormPublished, FormFilled, FieldAnswer, Question

log = logging.getLogger(__name__)

##################
# Parent Stuff

def parents_event(request, slug):
    try:
        event = EventForParents.objects.get(slug=slug)  # @UndefinedVariable get
    except ObjectDoesNotExist:
        raise Http404
    context = RequestContext(request, locals())
    return render_to_response('bccf/event.html', {}, context_instance=context)


@require_parent
@never_cache
def parents_event_signup(request, slug):
    event = EventForParents.objects.get(slug=slug)
    # Since we might have arrived through a membership-purchase page, let's clear the session variable that brought us here.
    if 'aftercheckout' in request.session:
        del request.session['aftercheckout']
    context = RequestContext(request, locals())
    return render_to_response('bccf/event_signup.html', {}, context_instance=context)
    
@require_parent
@never_cache
def parents_event_create(request):
    """
    View for creating an event as a parent.
    """
    if request.method == 'POST':
        form = ParentEventForm(request.POST)
        if form.is_valid():
            event = form.save()
            return redirect('/parents/event/%s' % (event.slug))
    else:
        form = ParentEventForm
    context = RequestContext(request, locals())
    return render_to_response('bccf/event_create.html', {}, context_instance=context)

#####################
# Professional Stuff

def professionals_event(request, slug):
    try:
        event = EventForProfessionals.objects.get(slug=slug)  # @UndefinedVariable get
    except ObjectDoesNotExist:
        raise Http404
    context = RequestContext(request, locals())
    return render_to_response('bccf/event.html', {}, context_instance=context)

@require_professional    
@never_cache
def professionals_event_signup(request, slug):
    event = EventForProfessionals.objects.get(slug=slug)
    # Since we might have arrived through a membership-purchase page, let's clear the session variable that brought us here.
    if 'aftercheckout' in request.session:
        del request.session['aftercheckout']
    context = RequestContext(request, locals())
    return render_to_response('bccf/event_signup.html', {}, context_instance=context)
    
# For Professional Event Wizard
FORMS = [('event', ProfessionalEventForm), # Main Form
         ('before', FormStructureSurveyFormOne), # Before Survey
         ('after', FormStructureSurveyFormTwo)] # After Survey
# Custom templates for each step
TEMPLATES = {'event': 'bccf/wizard_event_create.html',
             'before': 'generic/includes/form_builder.html',
             'after': 'generic/includes/form_builder.html'}
    
#@require_professional
#@never_cache
class ProfessionalEventWizard(SessionWizardView):
    """
    Form Wizard for creating a new professional event
    
    Steps: Event Details -> Before Survey (Optional) -> After Survey (Optional)
    """
    def get_template_names(self):
        """
        Override of form wizard's `get_template_names`
        
        Returns the proper template depending on step
        """
        return [TEMPLATES[self.steps.current]]
                
    def process_step(self, form):
        """
        Override of form wizard's `process_step`
        
        Process a step when a form is submitted. The values in the form are clean and valid
        """
        if self.steps.current == 'event': # Event form?
            if 'event-survey' in form.data and len(self.form_list) == 1: # Put back the deleted surveys if deleted before
                self.form_list['before'] = FORMS['before']
                self.form_list['after'] = FORMS['after']
            elif 'event-survey' not in form.data and len(self.form_list) == 3: # No Surveys delete the survey forms
                del self.form_list['before']
                del self.form_list['after']
        elif self.steps.current == 'before': # Before Survey form?
            if 'before-after_survey' in form.data and len(self.form_list) == 2: # After survey
                self.form_list['after'] = FORMS['after']
            elif 'before-after_survey' not in form.data and len(self.form_list) == 3: # No After Survey
                del self.form_list['after']
        return self.get_form_step_data(form)
    
    def get_context_data(self, form, **kwargs):
        """
        Override of form wizard's `get_context_data`
        
        Adds form_structure to context for cloning before survey
        """
        context = super(ProfessionalEventWizard, self).get_context_data(form=form, **kwargs)
        if self.steps.current == 'before': # Rebuild the form just in case the user goes back a step
            before_data = self.get_cleaned_data_for_step(step=self.steps.current)
            if before_data is not None and 'structure' in before_data:
                context.update({'form_structure':before_data['structure']})
        elif self.steps.current == 'after':
            before_data = self.get_cleaned_data_for_step(step='before')
            after_data = self.get_cleaned_data_for_step(step='after')
            if before_data['clone']: # Clone the before form?
                context.update({'form_structure':before_data['structure']})
            elif after_data is not None and 'structure' in after_data: # Rebuild the form just in case there's an error
                context.update({'form_structure':after_data['structure']})
        return context
    
    def done(self, form_list, **kwargs):
        """
        This is where the forms will be saved! If there are surveys, associate
        them with the Event. Form structures will be automatically published.
        
        REQUIRED by form wizard
        """
        event_data = form_list[0].cleaned_data
        if 'survey' in event_data: # check and remove the survey key-value pair
            del event_data['survey']
        if len(form_list) >= 2: # If there's a before survey
            event_data.update({'survey_before':self.process_survey(form_list[1])})
        if len(form_list) == 3: # If there's an after survey
            event_data.update({'survey_after':self.process_survey(form_list[2])})
            
        event = EventForProfessionals.objects.create(**event_data)
        return redirect('/professionals/event/%s' % (event.slug))            
    
    def process_survey(self, form):
        """
        Process each survey form and publishes them automatically.
        
        This is an almost copy of the publish view found in formable.builder.views
        """
        data = form.cleaned_data
        if 'clone' in data: # check and remove the clone key-value pair
            del data['clone']
        if 'after_survey' in data: # check and remove the after_survey key-value pair
            del data['after_survey']
        form_struct = FormStructure.objects.create(**data)
        published = FormPublished(form_structure=form_struct, user=self.request.user)
        published.save()
        
        # Create Questions based on structure
        struct = json.loads(form_struct.structure)
        for fieldset in struct["fieldset"]:
            for field in fieldset["fields"]:
                if "label" in field: # don't save static text
                    if "required" in field["attr"]:
                        required = 0
                    else:
                        required = 1
                        
                    if "options" in field:
                        num_answers = len(field["options"])
                        
                    question = Question(question=field["label"], 
                        form_published=published, required=required,
                        num_answers=len(field["options"]) or '')
                    question.save()
        # End Create Questions
        
        return published # FormPublished object
        
######################################
# Survey Report
def professional_survey_download_report(request, slug):
    """
    Downloads a CSV file of the survey results
    """
    if not request.user.is_authenticated():
        return redirect('/')
        
    try:
        event = EventForProfessionals.objects.get(slug=slug)
    except ObjectDoesNotExist:
        raise Http404
        
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s-%s-report.csv"' % (event.slug, time.strftime("%x"))
    
    writer = csv.writer(response)
    writer.writerow(['Report for %s' % (event.title)])
        
    if event.survey_before is not None:
        before_filled_forms = FormFilled.objects.filter(form_published=event.survey_before)
        headers = ['User Name', 'Date Filled']
        headers.extend(Question.objects.filter(form_published=event.survey_before))
        writer.writerow(headers)
        
        for form in before_filled_forms:
            answers = [form.user.get_full_name() or form.user.username, form.filled]
            answers.extend(FieldAnswer.objects.filter(form_filled=form))
            writer.writerow(answers)
        
    if event.survey_after is not None:
        writer.writerow(["After Survey"])
        after_filled_forms = FormFilled.objects.filter(form_published=event.survey_after)
        headers = ['User Name', 'Date Filled']
        headers.extend(Question.objects.filter(form_published=event.survey_after))
        writer.writerow(headers)
        
        for form in after_filled_forms:
            answers = [form.user.get_full_name() or form.user.username, form.filled]
            answers.extend(FieldAnswer.objects.filter(form_filled=form))
            writer.writerow(answers)

    #pass
    return response
