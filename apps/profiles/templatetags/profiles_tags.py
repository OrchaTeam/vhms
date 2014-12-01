from django import template

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