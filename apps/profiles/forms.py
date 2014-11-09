from django.conf import settings
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext, ugettext_lazy as _

from mezzanine.accounts.forms import ProfileForm
from mezzanine.accounts import get_profile_model


Profile = get_profile_model()

class VHMSSignupFormProfileFields(forms.ModelForm):
    """
    It identifies a list of fields are indicated in settings
    for Profile form.
    """

    class Meta:
        model = Profile
        fields = tuple(settings.VHMS_SIGNUP_PROFILE_FIELDS)


class VHMSProfileFormProfileFields(forms.ModelForm):
    """
    It identifies a list of fields are indicated in settings
    for Signup form.
    """

    class Meta:
        model = Profile
        fields = tuple(settings.VHMS_PROFILE_PROFILE_FIELDS)

class VHMSProfileForm(ProfileForm):
    """
    It generates Profile form for signup or profile view.
    """

    def __init__(self, *args, **kwargs):
        super(VHMSProfileForm, self).__init__(*args, **kwargs)
        self._signup = self.instance.id is None

        #update profile fields
        profile_fields_form = self.get_profile_fields_form()
        profile_fields = profile_fields_form().fields
        self.fields.update(profile_fields)

        if not self._signup:
            # profile form
            if "email" in self.fields:
                self.fields["email"].widget.attrs['readonly'] = True
        else:
            # signup form
            pass

    def get_profile_fields_form(self):
        if not self._signup:
            return VHMSProfileFormProfileFields
        else:
            return VHMSSignupFormProfileFields

# новое поколение форм
User = get_user_model()

class VHMSUserBaseForm(forms.ModelForm):
    """

    """

    class Meta:
        model = User
        fields = ("username", "email",)

    def __init__(self, *args, **kwargs):
        super(VHMSUserBaseForm, self).__init__(*args, **kwargs)
        if self.fields["username"]:
            self.fields["username"].label = "Username"
        if self.fields["email"]:
            self.fields["email"].label = "Email"


    def clean_username(self):
        """

        """

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
        """

        """
        email = self.cleaned_data["email"]
        qs = User.objects.filter(email=email)
        if len(qs) == 0:
            return email
        raise forms.ValidationError(_("This email is already registered"))

class VHMSUserSignupForm(VHMSUserBaseForm):
    """

    """

    password1 = forms.CharField(label=_("Password"),
        required=False,
        widget=forms.PasswordInput(
        render_value=False,
        attrs={'autocomplete': 'off;'}))
    password2 = forms.CharField(label=_("Password (again)"),
        widget=forms.PasswordInput(
        render_value=False,
        attrs={'autocomplete': 'off;'}))

    def __init__(self, *args, **kwargs):
        super(VHMSUserSignupForm, self).__init__(*args, **kwargs)
        self.fields["username"].required = True
        self.fields["email"].required = True


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

class VHMSPasswordChange(forms.ModelForm):

    password1 = forms.CharField(label=_("New password"),
        widget=forms.PasswordInput(
        render_value=False,
        attrs={'autocomplete': 'off;'}))
    password2 = forms.CharField(label=_("New password (again)"),
        widget=forms.PasswordInput(
        render_value=False,
        attrs={'autocomplete': 'off;'}))

    class Meta:
        model = User
        fields = ()

    def __init__(self, *args, **kwargs):
        super(VHMSPasswordChange, self).__init__(*args, **kwargs)
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

class VHMSExtendPasswordChange(VHMSPasswordChange):

    old_password = forms.CharField(label=_("Old password"),
        widget=forms.PasswordInput(
        render_value=False))

    def clean_old_password(self):

        old_password = self.cleaned_data.get("old_password")
        if old_password:
            if not self.user.check_password(old_password):
                raise forms.ValidationError(
                                ugettext("Old password is incorrect. "))
        return old_password