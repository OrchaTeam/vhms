from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.messages import info, error
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import View, RedirectView, TemplateView
from django.conf import settings
from django.core.urlresolvers import reverse, get_script_prefix
from django.contrib.auth.decorators import login_required

from apps.utils.email import send_verification_mail
from apps.utils.views import render
from apps.profiles import forms
from apps.utils.urls import next_url, login_redirect
from config import views_settings as views_names

# { TO DO: 050420151508 refactoring. get and post methods need to merge }

class VHMSUserSignupView(View):
    """

    """
    template_name = "profiles/account_signup.html"
    title = _("Sign up")

    def get(self, request):
        form = forms.VHMSUserSignupForm()
        context = {"form": form, "title": self.title}
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
                return redirect(next_url(request) or views_names.VHMS_CORE_HOME)
            else:
                info(request, _("Successfully signed up"))
                login(request, new_user)
                return login_redirect(request)
        context = {"form": form, "title": self.title}
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
            self.form = forms.VHMSExtendUserPasswordChangeForm(data=request.POST or None, instance=request.user)
            return {'title': _("Account Settings"),
                    'redirect_link': views_names.VHMS_PROFILE_ACCOUNT_SETTINGS,
                    'template': "profiles/profiles_account_settings.html"}
        else:
            self.form = forms.VHMSUserPasswordChangeForm(data=request.POST or None, instance=request.user)
            return {'title': _("Update Password"),
                    'redirect_link': views_names.VHMS_CORE_HOME,
                    'template': "profiles/account_password_change.html"}

class VHMSUserPasswordVerifyRedirectView(RedirectView):
    """
    It redirects when the "Reset Password" scenario is using.
    """

    def get_redirect_url(self, *args, **kwargs):
        uidb36, token = self.kwargs['uidb36'], self.kwargs['token']
        if uidb36 and token:
            profile = authenticate(uidb36=uidb36, token=token, is_active=True)
            if profile is not None:
                login(self.request, profile)
            else:
                error(self.request, _("The link you clicked is no longer valid."))
            return reverse(views_names.VHMS_PROFILE_PASSWORD_CHANGE)


class VHMSUserLoginView(View):
    """

    """
    template_name = "profiles/account_signup.html"
    title = _("Sign in")

    def get(self, request):
        form = forms.VHMSUserLoginForm()
        context = {"form": form, "title": self.title}
        return render(request, self.template_name, context)

    def post(self,request):
        form = forms.VHMSUserLoginForm(request.POST or None)
        if form.is_valid():
            authenticated_user = form.save()
            info(request, _("Successfully logged in"))
            login(request, authenticated_user)
            return login_redirect(request)
        context = {"form": form, "title": self.title}
        return render(request, self.template_name, context)


class VHMSUserLogoutView(View):
    """

    """

    def get(self,request):
        logout(request)
        info(request, _("Successfully logged out"))
        return redirect(next_url(request) or get_script_prefix())


class VHMSUserProfileView(TemplateView):
    """

    """
    template_name = "profiles/profiles_update.html"
    title = _("Update Profile")

    def get(self, request, *args, **kwargs):
        form = forms.VHMSUserProfileForm(instance=request.user.profile)
        context = {"form": form, "title": self.title}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = forms.VHMSUserProfileForm(
            data=request.POST,
            files=request.FILES,
            instance=request.user.profile)
        context = {"form": form, "title": self.title}
        if form.is_valid():
            form.save()
            info(request, _("Profile has been updated"))
        return render(request, self.template_name, context)


class VHMSUserPasswordResetView(TemplateView):
    """

    """
    template_name = "profiles/account_password_reset.html"
    title = _("Reset Password")

    def get(self, request, *args, **kwargs):
        form = forms.VHMSUserPasswordResetForm()
        context = {"form": form, "title": self.title}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = forms.VHMSUserPasswordResetForm(request.POST)
        if form.is_valid():
            profile = form.save()
            send_verification_mail(request, profile, "password_reset_verify")
            info(request, _("A verification email has been sent with "
                            "a link for resetting your password."))
        context = {"form": form, "title": self.title}
        return render(request, self.template_name, context)


def signup_verify(request, uidb36=None, token=None):
    """

    """
    profile = authenticate(uidb36=uidb36, token=token, is_active=False)
    if profile is not None:
        profile.is_active = True
        profile.save()
        login(request, profile)
        info(request, _("Successfully signed up"))
        return login_redirect(request)
    else:
        error(request, _("The link you clicked is no longer valid."))
        return redirect(views_names.VHMS_CORE_HOME)


signup = VHMSUserSignupView.as_view()
signin = VHMSUserLoginView.as_view()
signout = VHMSUserLogoutView.as_view()
password_change = login_required(VHMSUserPasswordChangeView.as_view())
password_reset = VHMSUserPasswordResetView.as_view()
password_reset_verify = VHMSUserPasswordVerifyRedirectView.as_view()
profile_update = login_required(VHMSUserProfileView.as_view())