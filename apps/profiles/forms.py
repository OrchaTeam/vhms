from django.conf import settings
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth import authenticate
from django.db.models import Q

from .models import Profile


class VHMSUserBaseForm(forms.ModelForm):
    """
    It is the base form for users profile. Base clean() methods are defined here.
    """

    class Meta:
        model = Profile
        fields = ("username", "email", "first_name", "last_name",)

    def __init__(self, *args, **kwargs):
        super(VHMSUserBaseForm, self).__init__(*args, **kwargs)

        if "username" in self.fields:
            self.fields["username"].label = _("Username")
        if "email" in self.fields:
            self.fields["email"].label = _("Email")
        if "first_name" in self.fields:
            self.fields["first_name"].label = _("First Name")
        if "last_name" in self.fields:
            self.fields["last_name"].label = _("Last Name")

        for field in self.fields:
            self.fields[field].required = True


    def clean_username(self):
        username = self.cleaned_data.get("username")
        USERNAME_REGEX = UserCreationForm().fields['username'].regex
        if not USERNAME_REGEX.match(username):
            raise forms.ValidationError(_("Usernames can only contain "
                                          "letters, digits and @/./+/-/_."))

        if username in settings.USER_BLACKLIST:
            raise forms.ValidationError(_("Username can not be used. "
                                          "Please use other username."))

        try:
            query = {'username__iexact': username}
            Profile.objects.get(**query)
        except Profile.DoesNotExist:
            return username
        raise forms.ValidationError(_("This username is already taken. Please "
                                      "choose another."))

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = Profile.objects.filter(email=email)
        if len(qs) == 0:
            return email
        raise forms.ValidationError(_("This email is already registered"))

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")

        if first_name.lower() not in settings.USER_BLACKLIST:
            return first_name
        raise forms.ValidationError(_("First name can not be used. "
                                      "Please use other username."))

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")

        if last_name.lower() not in settings.USER_BLACKLIST:
            return last_name
        raise forms.ValidationError(_("Last name can not be used. "
                                      "Please use other username."))

class VHMSUserPasswordBaseForm(forms.ModelForm):
    """
    It is the base form for a number of password forms.
    """

    password1 = forms.CharField(
        label=_("Password"),
        required=True,
        widget=forms.PasswordInput(
            render_value=False,
            attrs={'autocomplete': 'off;'})
    )
    password2 = forms.CharField(
        label=_("Password (again)"),
        widget=forms.PasswordInput(
            render_value=False,
            attrs={'autocomplete': 'off;'})
    )

    class Meta:
        model = Profile
        fields = ()

    def clean_password2(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]

        if password1:
            errors = []
            if password1 != password2:
                errors.append(_("Passwords do not match. "))
            if len(password1) < settings.USER_MIN_PASSWORD_LENGTH:
                errors.append(
                        _("Password must be at least %s characters. ") %
                        settings.USER_MIN_PASSWORD_LENGTH)
            if errors:
                self._errors["password1"] = self.error_class(errors)
        return password2


class VHMSUserSignupForm(VHMSUserBaseForm, VHMSUserPasswordBaseForm):
    """
    View: SignupView.
    The clean() methods and fields are inherited from parents:
    VHMSUserBaseForm and VHMSUserPasswordBaseForm.
    """

    def __init__(self, *args, **kwargs):
        super(VHMSUserSignupForm, self).__init__(*args, **kwargs)

    def save(self, **kwargs):
        kwargs["commit"] = False
        profile = super(VHMSUserSignupForm, self).save(**kwargs)
        profile.is_active = False
        if 'password1' in self.cleaned_data:
            profile.set_password(self.cleaned_data["password1"])
        else:
             raise forms.ValidationError(_("Internal error. "
                                           "Please, try again later."))
        profile.save()
        return profile


class VHMSUserPasswordChangeForm(VHMSUserPasswordBaseForm):
    """
    View: PasswordChangeView.
    The form is using for the remembering of password case.
    Fields and clean() methods are inherited from
    parent base form.
    """

    def __init__(self, *args, **kwargs):
        super(VHMSUserPasswordChangeForm, self).__init__(*args, **kwargs)
        if self.instance.id:
            self.profile = Profile.objects.get(id=self.instance.id)

    def save(self, *args, **kwargs):
        password = self.cleaned_data.get("password1")
        if password:
            self.profile.set_password(password)
        self.profile.save()


class VHMSExtendUserPasswordChangeForm(VHMSUserPasswordChangeForm):
    """
    View: PasswordChangeView.
    The form is using for the changing of password case.
    Fields and clean() methods are inherited from
    parent base form.
    """

    old_password = forms.CharField(
        label=_("Old password"),
        required=True,
        widget=forms.PasswordInput(
            render_value=False,
            attrs={'autocomplete': 'off;'})
    )

    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password")
        if old_password:
            if not self.user.check_password(old_password):
                raise forms.ValidationError(
                                ugettext("Old password is incorrect. "))
        return old_password


class VHMSUserLoginForm(forms.Form):
    """
    View: LoginView.
    The form is using for the login case.
    """

    username = forms.CharField(label=_("Username or Email"))
    password = forms.CharField(
        label=_("Password"),
        required=True,
        widget=forms.PasswordInput(
            render_value=False,
            attrs={'autocomplete': 'off;'}))

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        self._user = authenticate(username=username, password=password)
        if self._user is None:
            raise forms.ValidationError(
                             _("Invalid username/email and password"))
        elif not self._user.is_active:
            raise forms.ValidationError(_("Your account is inactive"))
        return self.cleaned_data

    def save(self):
        return getattr(self, "_user", None)


class VHMSUserProfileForm(VHMSUserBaseForm):
    """
    View: ProfileView.
    The form is using for the updating profile
    and reading profile case.
    Fields and clean() methods are inherited from
    parent base form.
    """

    class Meta:
        model = Profile
        fields = ("first_name", "last_name", )


class VHMSUserPasswordResetForm(forms.Form):
    """
    View: ResetPasswordView.
    """

    username_or_email = forms.CharField(
        label=_("Username or Email"))

    def clean(self):
        input = self.cleaned_data.get("username_or_email")
        username_or_email = Q(username=input) | Q(email=input)
        try:
            profile = Profile.objects.get(username_or_email, is_active=True)
        except Profile.DoesNotExist:
            raise forms.ValidationError(
                ugettext("Invalid username/email"))
        else:
            self._profile = profile
        return self.cleaned_data

    def save(self):
        """
        Just return the authenticated user - used for sending login
        email.
        """
        return getattr(self, "_profile", None)

