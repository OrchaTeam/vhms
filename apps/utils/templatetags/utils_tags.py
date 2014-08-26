from django import template

from apps.utils import utils

register = template.Library()

@register.simple_tag(takes_context=True, name='active')
def active(context, view):
    """
    It returns the 'active' string for a current and reverse url path.
    """
    request = context['request']
    return utils.ActiveMenu(request, view).is_active