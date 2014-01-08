from django import template

register = template.Library()

@register.filter(name='add')
def add(value, to_add):
    return value + to_add