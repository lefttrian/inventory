from django import template
from django.db.models import Sum

register = template.Library()

@register.simple_tag
def get_verbose_field_name(obj, field):
    """
    Returns verbose_name for a field.
    """
    try:
        return obj._meta.get_field(field).verbose_name
    except:
        return field

@register.simple_tag
def get_help_text(obj, field):
    """
    Returns help_text for a field.
    """
    try:
        return obj._meta.get_field(field).help_text
    except:
        return field


@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)

