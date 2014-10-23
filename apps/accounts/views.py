from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.messages import info, error
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.views.generic.base import View, RedirectView

from mezzanine.utils.views import render

from .forms import VHMSPasswordChange, VHMSExtendPasswordChange

class VHMSPasswordChangeView(View):
    """
    It generates view for password change in "Account Settings" and "Reset Password"
    scenarios. Forms are creating by the init_form method. This method is looking for
    a current url path to indicate the current scenario.
    """

    def get(self, request):
        obj = self.init_form(request)
        return render(request, obj['template'], {'form': self.form, 'title': obj['title']})

    def post(self, request):
        obj = self.init_form(request)
        if self.form.is_valid():
            self.form.save()
            info(request, _("Password has been changed"))
            return redirect(obj['redirect_link'])
        return render(request, obj['template'], {'form': self.form, 'title': obj['title']})

    def init_form(self, request):
        if request.path == reverse("account_settings"):
            self.form = VHMSExtendPasswordChange(data=request.POST or None, instance=request.user)
            return {'title': _("Account Settings"),
                    'redirect_link': "account_settings",
                    'template': "profiles/profiles_account_settings.html"}
        else:
            self.form = VHMSPasswordChange(data=request.POST or None, instance=request.user)
            return {'title': _("Update Password"),
                    'redirect_link': "home",
                    'template': "accounts/account_password_change.html"}

class VHMSPasswordVerifyRedirectView(RedirectView):
    """
    It redirects when the "Reset Password" scenario is using.
    """

    def get_redirect_url(self, *args, **kwargs):
        uidb36, token = self.kwargs['uidb36'], self.kwargs['token']
        if uidb36 and token:
            user = authenticate(uidb36=uidb36, token=token, is_active=True)
            if user is not None:
                login(self.request, user)
                return reverse('password_change')
            else:
                error(self.request, _("The link you clicked is no longer valid."))
                return reverse('home')

password_change = VHMSPasswordChangeView.as_view()
password_reset_verify = VHMSPasswordVerifyRedirectView.as_view()
