from mezzanine.accounts.forms import ProfileForm

class VHMSProfileForm(ProfileForm):

    def __init__(self, *args, **kwargs):
        super(VHMSProfileForm, self).__init__(*args, **kwargs)


