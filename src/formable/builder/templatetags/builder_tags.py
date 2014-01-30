from django import template

from formable.builder.forms import FormStructureForm, ListForPublishForm

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
    
@register.inclusion_tag("form_utils/list_forms.html", takes_context=True)
def form_list_for_publish(context):
    """
    Provides a generic context variable to render a form struct list.
    """
    context["list_form"] = ListForPublishForm()
    return context
