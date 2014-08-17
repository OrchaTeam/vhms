from django import forms
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from mezzanine.utils.models import get_user_model

User = get_user_model()

class VHMSPasswordChange(forms.ModelForm):

    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(label=_("Password (again)"),
                                widget=forms.PasswordInput(render_value=False))

    class Meta:
        model = User
        fields = ()

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
        kwargs["commit"] = False
        user = super(VHMSPasswordChange, self).save(*args, **kwargs)

        password = self.cleaned_data.get("password1")
        if password:
            user.set_password(password)
        user.save()
