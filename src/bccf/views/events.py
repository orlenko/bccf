import logging
import json
import csv
import time

from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from django.contrib.formtools.wizard.views import SessionWizardView
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse

from bccf.models import EventForParents, EventForProfessionals, BCCFPage
from bccf.util.memberutil import require_parent, require_professional
from bccf.forms import ProfessionalEventForm, FormStructureSurveyFormOne, FormStructureSurveyFormTwo
from django.views.decorators.cache import never_cache

from formable.builder.models import FormStructure, FormPublished, FormFilled, FieldAnswer, Question

log = logging.getLogger(__name__)

##################
# Generic Stuff
def event_page(request):
    page = BCCFPage.objects.get(slug='trainings')
    context = RequestContext(request, locals())
    return render_to_response('bccf/events_page.html', {}, context_instance=context)


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
        log.info(form_list)
        event = form_list[0].save()
        if len(form_list) >= 2: # If there's a before survey
            event.survey_before = form_list[1].save(self.request.user)
            event.survey_before.gparent = None
            event.survey_before.parent = None
            event.survey_before.save()
        if len(form_list) == 3: # If there's an after survey
            event.survey_after = form_list[2].save(self.request.user)
            event.survey_after.gparent = None
            event.survey_after.parent = None
            event.survey_after.save()

        event.save()

        return redirect(event.get_absolute_url())

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

    counter = 0
    current = None

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s-%s-report.csv"' % (event.slug, time.strftime("%x"))

    writer = csv.writer(response)
    writer.writerow(['Report for %s' % (event.title)])

    rows = {'Name':[], 'Date':[]}

    if event.survey_before is not None: # If there's a before Survey
        before_filled_forms = FormFilled.objects.filter(form_published=event.survey_before)
        questions = Question.objects.filter(form_published=event.survey_before)
        for question in questions:
            if question.num_answers == 0:
                question_key = 'Q-%s-%s' % (question.question,str(question.num_answers))
                if question_key not in rows:
                    rows.update({question_key:[]})
            else:
                for x in range(0, question.num_answers):
                    question_key = 'Q-%s-%s' % (question.question,str(x))
                    if question_key not in rows:
                        rows.update({question_key:[]})
        for form in before_filled_forms:
            rows['Name'].append(form.user.get_full_name() or form.user.username)
            rows['Date'].append(form.filled)
            answers = FieldAnswer.objects.filter(form_filled=form)
            for answer in answers:
                if current is None or current != answer.question:
                    counter = 0
                    current = answer.question
                elif current == answer.question:
                    counter += 1
                rows['Q-%s-%s' % (current.question, str(counter))].append(answer.answer)
            for row in rows:
                if len(rows[row]) < len(rows['Name']):
                    rows[row].append('')

    if event.survey_after is not None: # If there's an after Survey
        after_filled_forms = FormFilled.objects.filter(form_published=event.survey_after)
        questions = Question.objects.filter(form_published=event.survey_after)
        for question in questions:
            if question.num_answers == 0:
                question_key = 'Q-%s-%s' % (question.question,str(question.num_answers))
                if question_key not in rows:
                    rows.update({question_key:['']*len(after_filled_forms)})
            else:
                for x in range(0, question.num_answers):
                    question_key = 'Q-%s-%s' % (question.question,str(x))
                    if question_key not in rows:
                        rows.update({question_key:[' ']*len(rows['Name'])})
        for form in after_filled_forms:
            rows['Name'].append(form.user.get_full_name() or form.user.username)
            rows['Date'].append(form.filled)
            answers = FieldAnswer.objects.filter(form_filled=form)
            for answer in answers:
                if current is None or current != answer.question:
                    counter = 0
                    current = answer.question
                elif current == answer.question:
                    counter += 1
                rows['Q-%s-%s' % (current.question, str(counter))].append(answer.answer)
            for row in rows:
                if len(rows[row]) < len(rows['Name']):
                    rows[row].append('')

    rows['Name'].insert(0, 'Name')
    rows['Date'].insert(0, 'Date')
    writer.writerow(rows['Name'])
    writer.writerow(rows['Date'])
    del rows['Name']
    del rows['Date']

    for key,val in reversed(rows.items()):
        val.insert(0, key[:key.rfind('-')])
        writer.writerow(val)
    #pass
    return response

