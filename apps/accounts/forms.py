from django import forms
from django.utils.translation import ugettext_lazy as _, ugettext
from django.conf import settings

from mezzanine.utils.models import get_user_model

User = get_user_model()

class VHMSPasswordChange(forms.ModelForm):

    password1 = forms.CharField(label=_("New password"),
                                widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(label=_("New password (again)"),
                                widget=forms.PasswordInput(render_value=False))
    # {WORKAROUND: clear and replace to variables}
    password1.widget.attrs["autocomplete"] = "off"
    password2.widget.attrs["autocomplete"] = "off"

    class Meta:
        model = User
        fields = ()

    def __init__(self, *args, **kwargs):
        super(VHMSPasswordChange, self).__init__(*args, **kwargs)
        self.user = User.objects.get(id=self.instance.id)

    def clean_password2(self):

        
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1:
            errors = []
            if password1 != password2:
                errors.append(_("Passwords do not match. "))
            if len(password1) < settings.ACCOUNTS_MIN_PASSWORD_LENGTH:
                errors.append(
                        _("Password must be at least %s characters. ") %
                        settings.ACCOUNTS_MIN_PASSWORD_LENGTH)
            if errors:
                self._errors["password1"] = self.error_class(errors)
        return password2

    def save(self, *args, **kwargs):

        password = self.cleaned_data.get("password1")
        if password:
            self.user.set_password(password)
        self.user.save()

class VHMSExtendPasswordChange(VHMSPasswordChange):

    old_password = forms.CharField(label=_("Old password"), widget=forms.PasswordInput(render_value=False))

    def clean_old_password(self):
        
        old_password = self.cleaned_data.get("old_password")
        if old_password:
            if not self.user.check_password(old_password):
                raise forms.ValidationError(
                                ugettext("Old password is incorrect. "))
        return old_password