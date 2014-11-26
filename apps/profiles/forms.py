from django.conf import settings
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth import authenticate

from .models import Profile

User = get_user_model()

class VHMSUserBaseForm(forms.ModelForm):
    """

    """

    class Meta:
        model = Profile
        fields = ("username", "email", "first_name", "last_name",)

    def __init__(self, *args, **kwargs):
        super(VHMSUserBaseForm, self).__init__(*args, **kwargs)
        instance = self.instance.id or None
        if instance:
            self.profile = Profile.objects.get(id=instance)
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
            User.objects.get(**query)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(_("This username is already taken. Please "
                                      "choose another."))

    def clean_email(self):
        email = self.cleaned_data["email"]
        qs = User.objects.filter(email=email)
        if len(qs) == 0:
            return email
        raise forms.ValidationError(_("This email is already registered"))

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")

        if first_name in settings.USER_BLACKLIST:
            raise forms.ValidationError(_("First name can not be used. "
                                          "Please use other username."))

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")

        if last_name in settings.USER_BLACKLIST:
            raise forms.ValidationError(_("Last name can not be used. "
                                          "Please use other username."))

class VHMSUserSignupForm(VHMSUserBaseForm):
    """

    """

    password1 = forms.CharField(label=_("Password"),
        required=True,
        widget=forms.PasswordInput(
            render_value=False,
            attrs={'autocomplete': 'off;'}))
    password2 = forms.CharField(label=_("Password (again)"),
        widget=forms.PasswordInput(
            render_value=False,
            attrs={'autocomplete': 'off;'}))

    def __init__(self, *args, **kwargs):
        super(VHMSUserSignupForm, self).__init__(*args, **kwargs)

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

    # {WORKAROUND: *args **kwargs?!?!}
    def save(self, *args, **kwargs):
        kwargs["commit"] = False
        user = super(VHMSUserSignupForm, self).save(*args, **kwargs)
        user.is_active = False
        if 'password1' in self.cleaned_data:
            user.set_password(self.cleaned_data["password1"])
        else:
             raise forms.ValidationError(_("Internal error. Please, try again later."))
        user.save()
        return user


class VHMSUserPasswordChangeForm(forms.ModelForm):

    password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(
            render_value=False,
            attrs={'autocomplete': 'off;'}))
    password2 = forms.CharField(label=_("New password (again)"),
        widget=forms.PasswordInput(
            render_value=False,
            attrs={'autocomplete': 'off;'}))

    class Meta:
        model = Profile
        fields = ()

    def __init__(self, *args, **kwargs):
        super(VHMSUserPasswordChangeForm, self).__init__(*args, **kwargs)
        if self.instance.id:
            self.user = User.objects.get(id=self.instance.id)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

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

    def save(self, *args, **kwargs):
        password = self.cleaned_data.get("password1")
        if password:
            self.user.set_password(password)
        self.user.save()


class VHMSExtendUserPasswordChangeForm(VHMSUserPasswordChangeForm):

    old_password = forms.CharField(
        label=_("Old password"),
        widget=forms.PasswordInput(
            render_value=False))

    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password")
        if old_password:
            if not self.user.check_password(old_password):
                raise forms.ValidationError(
                                ugettext("Old password is incorrect. "))
        return old_password


class VHMSUserLoginForm(forms.Form):
    """

    """

    username = forms.CharField(label=_("Username or Email"))
    password = forms.CharField(label=_("Password"),
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


class VHMSProfileForm(VHMSUserBaseForm):
    """

    """


    class Meta:
        model = Profile
        fields = ("first_name", "last_name",)

    def save(self, commit=True):
        self.profile.save()
        return self.profile