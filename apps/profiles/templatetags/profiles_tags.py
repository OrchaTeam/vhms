from django import template
from django.utils.translation import ugettext_lazy as _

register = template.Library()

@register.filter
def get_profile(profile, attr):
    """

    """
    value = _("Profile: ")
    if hasattr(profile, attr):
        value = getattr(profile, attr)
        if callable(value):
            value += value()
    return value