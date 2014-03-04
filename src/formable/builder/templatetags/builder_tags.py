from django import template

from formable.builder.forms import FormStructureForm, CloneFormForm

import logging

log = logging.getLogger(__name__)

register = template.Library()

@register.inclusion_tag("builder.html", takes_context=True)
def builder(context):
    """
    Provides a generic context variable to render a form builder.
    """
    context["structure_form"] = FormStructureForm()
    return context

@register.inclusion_tag("form_utils/list_clone.html", takes_context=True)
def form_clone_for_event(context, event):
    context['event'] = event
    context["list_clone"] = FormStructure.objects.filter(Q(user=None) | Q(user=event.provider)).order_by('user')
    return context