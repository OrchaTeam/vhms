from django.utils.http import is_safe_url
from django.shortcuts import redirect
from django.conf import settings

def next_url(request):
    """
    It was replaced from Mezzanine 3.1.9.
    Returns URL to redirect to from the ``next`` param in the request.
    """
    next = request.REQUEST.get("next", "")
    host = request.get_host()
    return next if next and is_safe_url(next, host=host) else None

def login_redirect(request):
    """
    It was replaced from Mezzanine 3.1.9.
    The part of logic was changed.
    Returns the redirect response for login/signup. Favors:
    - next param
    - LOGIN_REDIRECT_URL setting
    - homepage
    """

    ignorable_nexts = ("", settings.SIGNUP_URL, settings.LOGIN_URL, settings.LOGOUT_URL)
    next = next_url(request) or ""
    if next in ignorable_nexts:
        next = settings.LOGIN_REDIRECT_URL

    return redirect(next)