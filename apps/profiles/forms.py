from mezzanine.accounts.forms import ProfileForm
from mezzanine.conf import settings
from django import forms
from mezzanine.accounts import get_profile_model

Profile = get_profile_model()

class VHMSSignupForm(forms.ModelForm):

    class Meta:
        model = Profile
        exclude = tuple(settings.VHMS_SIGNUP_FORM_EXCLUDE_FIELDS)

class VHMSProfileForm (ProfileForm):

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self._signup = self.instance.id is None

        if self._signup:
            profile_fields = VHMSSignupForm().fields
            self.fields.update(profile_fields)
        else:
            self.get_profile_fields_form()
        

