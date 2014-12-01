from django.core.urlresolvers import reverse, NoReverseMatch

class VHMSActiveMenu(object):
    """
    It provides a view of an active tab for the menu.
    It works in the Profile app and need to test for
    other apps.
    """

    def __init__(self, request, view):

        self.is_active = ""
        try:
            if request.path == reverse(view):
                self.is_active = "active"
        except NoReverseMatch:
            pass