from django.conf import settings
from django import forms

from mezzanine.accounts.forms import ProfileForm
from mezzanine.accounts import get_profile_model

Profile = get_profile_model()

class VHMSSignupFormProfileFields(forms.ModelForm):

    class Meta:
        model = Profile
        fields = tuple(settings.VHMS_SIGNUP_PROFILE_FIELDS)


class VHMSProfileFormProfileFields(forms.ModelForm):

    class Meta:
        model = Profile
        fields = tuple(settings.VHMS_PROFILE_PROFILE_FIELDS)

class VHMSProfileForm(ProfileForm):

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