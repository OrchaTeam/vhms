from mezzanine.accounts.forms import ProfileForm
from mezzanine.utils.models import get_user_model
from django.conf import settings
from django import forms
from mezzanine.accounts import get_profile_model

User = get_user_model()
Profile = get_profile_model()

class VHMSSignupFormUserFields(forms.ModelForm):

    class Meta:
        model = User
        fields = tuple(settings.VHMS_SIGNUP_USER_FIELDS)


class VHMSProfileFormUserFields(forms.ModelForm):

    class Meta:
        model = User
        fields = tuple(settings.VHMS_PROFILE_USER_FIELDS)


class VHMSSignupFormProfileFields(forms.ModelForm):

    class Meta:
        model = Profile
        fields = tuple(settings.VHMS_SIGNUP_PROFILE_FIELDS)


class VHMSProfileFormProfileFields(forms.ModelForm):

    class Meta:
        model = Profile
        fields = tuple(settings.VHMS_PROFILE_PROFILE_FIELDS)

class VHMSProfileForm(ProfileForm):

    class Meta:
        model = User
        fields = ()
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(VHMSProfileForm, self).__init__(*args, **kwargs)
        self._signup = self.instance.id is None
        
        # update user fields
        user_fields_form = self.get_user_fields_form()
        user_fields = user_fields_form().fields
        self.fields.update(user_fields)

        #update profile fields
        profile_fields_form = self.get_profile_fields_form()
        profile_fields = profile_fields_form().fields
        self.fields.update(profile_fields)

        if not self._signup:
            # profile form
            if "email" in settings.VHMS_PROFILE_USER_FIELDS:
                self.fields["email"].widget.attrs['readonly'] = True
        else:
            # signup form
            pass
            
    def save(self, *args, **kwargs):
        super(VHMSProfileForm, self).save(*args, **kwargs)

    def get_user_fields_form(self):
        if not self._signup:
            return VHMSProfileFormUserFields
        else:
            return VHMSSignupFormUserFields

    def get_profile_fields_form(self):
        if not self._signup:
            return VHMSProfileFormProfileFields
        else:
            return VHMSSignupFormProfileFields