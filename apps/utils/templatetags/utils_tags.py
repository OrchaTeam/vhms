from django import template

from apps.utils import utils

register = template.Library()


@register.simple_tag(takes_context=True, name='active')
def active(context, view):
    """
    It returns the 'active' string for a current and reverse url path.
    """
    return utils.VHMSActiveMenu(context['request'], view).is_active