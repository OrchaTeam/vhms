from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.messages import info, error
from django.utils.translation import ugettext_lazy as _

from mezzanine.utils.views import render

from .forms import VHMSPasswordChange

def password_change(request, template=None):
    form = VHMSPasswordChange(data=request.POST or None, instance=request.user)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            info(request, _("Password has been changed"))
            return redirect("/")
        else:
            pass

    context = {"form": form, "title": _("Reset Password")}
    return render(request, template, context)

def password_reset_verify(request, uidb36=None, token=None):
    user = authenticate(uidb36=uidb36, token=token, is_active=True)
    if user is not None:
        login(request, user)
        return redirect("password_change")
    else:
        error(request, _("The link you clicked is no longer valid."))
        return redirect("/")