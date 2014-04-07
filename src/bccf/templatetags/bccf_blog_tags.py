from mezzanine import template

from bccf.models import Blog

register = template.Library()

@register.inclusion_tag('generic/includes/author.html', takes_context=True)
def author_for(context, obj):
    """
    Gets the author of if the object is a blog post
    """
    if obj._meta.object_name == 'BCCFChildPage':
        if obj.content_model == 'blog':
            context['author'] = obj.get_content_model().author
    return context