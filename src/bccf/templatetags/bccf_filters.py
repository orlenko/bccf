from django import template
from bccf import models

register = template.Library()

@register.filter(name='add')
def add(value, to_add):
    return value + to_add

@register.filter
def has_feature(membership, feature):
    feature_map = {
        'people': ('Membership: Organizations', 'Membership: Corporate'),
        'events': ('Membership: Professionals', 'Membership: Organizations', 'Admin'),
        'subscriptions': ('Membership: Professionals', 'Membership: Parents')
    }
    for categ in feature_map.get(feature, []):
        if models.is_product_variation_categ(membership, categ):
            return True

@register.filter
def get_class_name(value):
    return value.__class__.__name__