from django import template

from apps.utils import utils

register = template.Library()


@register.simple_tag(takes_context=True, name='active')
def active(context, view):
    """
    It returns the 'active' string for a current and reverse url path.
    """
    return utils.VHMSActiveMenu(context['request'], view).is_active

@register.simple_tag(takes_context=False, name='avatar')
def avatar(value, size=None):
    """
    It returns a view for avatar. size values: 'full', 'thumb'.
    full is original image; thumb is thumbnail
    :param value of avatar:
    :return: string for a view of avatar
    """
    return utils.VHMSProfileAvatarField(value, size).avatar