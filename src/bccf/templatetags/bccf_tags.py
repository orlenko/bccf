from django.template.base import Variable
from django.template.context import Context
from django.template.loader import get_template
from mezzanine import template


register = template.Library()


@register.render_tag
def bccf_pagination(context, token):
    parts = token.split_contents()[1:]
    for part in parts:
        recordlist = Variable(part).resolve(context)
        break
    context['recordlist'] = recordlist
    t = get_template('includes/pagination.html')
    return t.render(Context(context))
