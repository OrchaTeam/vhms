from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.messages import info, error
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import View, RedirectView
from django.conf import settings
from django.core.urlresolvers import reverse

from apps.utils.email import send_verification_mail
from apps.utils.views import render
from apps.profiles import forms
from apps.utils.urls import next_url, login_redirect


class VHMSUserSignupView(View):
    """

    """

    template_name = "accounts/account_signup.html"

    def get(self, request):
        form = forms.VHMSUserSignupForm()
        context = {"form": form, "title": _("Sign up")}
        return render(request, self.template_name, context)

    def post(self, request):
        form = forms.VHMSUserSignupForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            if not new_user.is_active:
                if settings.USER_VERIFICATION_REQUIRED:
                    send_verification_mail(request, new_user, "signup_verify")
                    info(request, _("A verification email has been sent with "
                                    "a link for activating your account."))
                return redirect(next_url(request) or "/")
            else:
                info(request, _("Successfully signed up"))
                login(request, new_user)
                return login_redirect(request)
        context = {"form": form, "title": _("Sign up")}
        return render(request, self.template_name, context)


class VHMSUserPasswordChangeView(View):
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
            self.form = forms.VHMSExtendPasswordChange(data=request.POST or None, instance=request.user)
            return {'title': _("Account Settings"),
                    'redirect_link': "account_settings",
                    'template': "profiles/profiles_account_settings.html"}
        else:
            self.form = forms.VHMSPasswordChange(data=request.POST or None, instance=request.user)
            return {'title': _("Update Password"),
                    'redirect_link': "home",
                    'template': "accounts/account_password_change.html"}


class VHMSUserPasswordVerifyRedirectView(RedirectView):
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


def signup_verify(request, uidb36=None, token=None):
    """

    """
    user = authenticate(uidb36=uidb36, token=token, is_active=False)
    if user is not None:
        user.is_active = True
        user.save()
        login(request, user)
        info(request, _("Successfully signed up"))
        return login_redirect(request)
    else:
        error(request, _("The link you clicked is no longer valid."))
        return redirect("/")


signup = VHMSUserSignupView.as_view()
password_change = VHMSUserPasswordChangeView.as_view()
password_reset_verify = VHMSUserPasswordVerifyRedirectView.as_view()