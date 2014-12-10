from django import template
from allauth.socialaccount import admin

register = template.Library()

@register.filter
def get_profile(user, attr):
    """

    """
    try:
        value = getattr(user, attr)
        if callable(value):
            value = value()
    except AttributeError:
        value = "Profile"
    return value