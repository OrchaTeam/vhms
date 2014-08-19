from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.messages import info, error
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse, NoReverseMatch

from mezzanine.utils.views import render

from .forms import VHMSPasswordChange, VHMSExtendPasswordChange

def password_change(request, template=None):

    form = VHMSPasswordChange(data=request.POST or None, instance=request.user)
    title = _("Update Password")
    try:
        if request.path == reverse("account_settings"):
            form, account_settings = VHMSExtendPasswordChange(data=request.POST or None, instance=request.user), True
            title = _("Account Settings")
    except NoReverseMatch:
        error(request, _("Internal Error. 0001"))
        
    if request.method == "POST" and form.is_valid():
        form.save()
        info(request, _("Password has been changed"))
        if account_settings:
            return redirect(reverse("account_settings"))
        return redirect("/")

    context = {"form": form, "title": title}
    return render(request, template, context)

def password_reset_verify(request, uidb36=None, token=None):
    user = authenticate(uidb36=uidb36, token=token, is_active=True)
    if user is not None:
        login(request, user)
        return redirect("password_change")
    else:
        error(request, _("The link you clicked is no longer valid."))
        return redirect("/")