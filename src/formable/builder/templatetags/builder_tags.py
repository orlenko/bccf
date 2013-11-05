from django import template

from formable.builder.forms import FormStructureForm

import logging

log = logging.getLogger(__name__)

register = template.Library()

@register.inclusion_tag("builder/builder.html", takes_context=True)
def builder_for(context, obj=None):
    """
    Provides a generic context variable name for the object that builders are
    being rendered for.
    """
    context["structure_form"] = FormStructureForm()
    return context
