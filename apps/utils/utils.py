from django.core.urlresolvers import reverse, NoReverseMatch
import settings

class VHMSActiveMenu(object):
    """
    It provides a view of an active tab for the menu.
    """

    def __init__(self, request, view):

        self.is_active = ""
        try:
            if request.path == reverse(view):
                self.is_active = "active"
        except NoReverseMatch:
            pass

class VHMSProfileAvatarField(object):
    """
    It provides a view for avatar.
    full is original avatar. thumb is a thumbnail
    """

    def __init__(self, value, size):
        if size == 'thumb':
            pass
        else:
            if value == "":
                self.avatar = '{% static "img/default-avatar.jpeg" %}'
            else:
                self.avatar = '%s%s'% (settings.MEDIA_URL, value)