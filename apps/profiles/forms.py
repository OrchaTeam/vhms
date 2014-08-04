from mezzanine.accounts.forms import ProfileForm, ProfileFieldsForm
from mezzanine.conf import settings
from django import forms
from mezzanine.accounts import get_profile_model, get_profile_user_fieldname
from mezzanine.utils.models import get_user_model

User = get_user_model()
Profile = get_profile_model()

class VHMSProfileFieldsForm(forms.ModelForm):

    class Meta:
        model = Profile
        exclude = (get_profile_user_fieldname(),) + tuple(settings.VHMS_PROFILE_FORM_EXCLUDE_FIELDS)

class VHMSProfileForm(ProfileForm):

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username")
        exclude = tuple(settings.VHMS_PROFILE_FORM_EXCLUDE_FIELDS)
    
    def __init__(self, *args, **kwargs):
        super(VHMSProfileForm, self).__init__(*args, **kwargs)

        self._signup = self.instance.id is None
        if not self._signup:
            profile_fields = VHMSProfileFieldsForm().fields
        else:
            profile_fields = ProfileFieldsForm().fields
        self.fields.update(profile_fields)