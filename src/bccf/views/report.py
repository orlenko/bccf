import csv
import logging
import time
from bccf.models import Event
from django.shortcuts import redirect
log = logging.getLogger(__name__)

from django.http import HttpResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required


from formable.builder.models import FormPublished, FormFilled, Question, FieldAnswer

@login_required
def survey_report(request, slug):
    try:
        published = FormPublished.objects.get(slug=slug)
    except ObjectDoesNotExist:
        log.info('Object Does Not Exist')
        raise Http404

    if not request.user.is_staff and not request.user.is_superuser and not published.user == request.user:
        log.info('Not Staff or Publish User')
        raise Http404

    counter = 0
    current = None

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s-%s-report.csv"' % (published.slug, time.strftime("%x"))

    writer = csv.writer(response)
    writer.writerow(['Report for %s' % (published.title)])

    rows = {'Name':[], 'Date':[]}

    before_filled_forms = FormFilled.objects.filter(form_published=published)
    questions = Question.objects.filter(form_published=published)
    for question in questions:
        if question.num_answers == 0:
            question_key = 'Q-%s-%d' % (question.question.replace(' ', '-'), question.num_answers)
            if question_key not in rows:
                rows.update({question_key:[]})
        else:
            for x in range(0, question.num_answers):
                question_key = 'Q-%s-%d' % (question.question.replace(' ', '-'), x)
                if question_key not in rows:
                    rows.update({question_key:[]})
    for form in before_filled_forms:
        rows['Name'].append(form.user.get_full_name() or form.user.username)
        rows['Date'].append(form.filled)
        answers = FieldAnswer.objects.filter(form_filled=form)
        current = None
        for answer in answers:
            if not current or current != answer.question:
                counter = 0
                current = answer.question
                log.debug('not same: %s' % answer.question)
            elif current == answer.question:
                counter += 1
                log.debug('same: %s' % answer.question)
            log.debug(rows)
            rows['Q-%s-%d' % (current.question.replace(' ', '-'), counter)].append(answer.answer)
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

@login_required
def event_survey_report(request, slug):
    """
    Downloads a CSV file of the survey results
    """
    if not request.user.is_authenticated():
        return redirect('/')

    try:
        event = Event.objects.get(slug=slug)
    except ObjectDoesNotExist:
        raise Http404

    if not request.user.is_staff and (event.survey_before and not event.survey_before.user == request.user):
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
                question_key = 'Q-%s-%d' % (question.question.replace(' ', '-'), question.num_answers)
                if question_key not in rows:
                    rows.update({question_key:[]})
            else:
                for x in range(0, question.num_answers):
                    question_key = 'Q-%s-%d' % (question.question.replace(' ', '-'), x)
                    if question_key not in rows:
                        rows.update({question_key:[]})
        for form in before_filled_forms:
            rows['Name'].append(form.user.get_full_name() or form.user.username)
            rows['Date'].append(form.filled)
            answers = FieldAnswer.objects.filter(form_filled=form)
            current = None
            for answer in answers:
                if current is None or current != answer.question:
                    counter = 0
                    current = answer.question
                elif current == answer.question:
                    counter += 1
                rows['Q-%s-%d' % (current.question.replace(' ', '-'), counter)].append(answer.answer)
            for row in rows:
                if len(rows[row]) < len(rows['Name']):
                    rows[row].append('')

    if event.survey_after is not None: # If there's an after Survey
        after_filled_forms = FormFilled.objects.filter(form_published=event.survey_after)
        questions = Question.objects.filter(form_published=event.survey_after)
        for question in questions:
            if question.num_answers == 0:
                question_key = 'Q-%s-%d' % (question.question.replace(' ', '-'), question.num_answers)
                if question_key not in rows:
                    rows.update({question_key:['']*len(after_filled_forms)})
            else:
                for x in range(0, question.num_answers):
                    question_key = 'Q-%s-%d' % (question.question.replace(' ', '-'), x)
                    if question_key not in rows:
                        rows.update({question_key:[' ']*len(rows['Name'])})
        for form in after_filled_forms:
            rows['Name'].append(form.user.get_full_name() or form.user.username)
            rows['Date'].append(form.filled)
            answers = FieldAnswer.objects.filter(form_filled=form)
            current = None
            for answer in answers:
                if current is None or current != answer.question:
                    counter = 0
                    current = answer.question
                elif current == answer.question:
                    counter += 1
                rows['Q-%s-%d' % (current.question.replace(' ', '-'), counter)].append(answer.answer)
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