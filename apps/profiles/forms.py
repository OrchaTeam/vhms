from mezzanine.accounts.forms import ProfileForm
from mezzanine.utils.models import get_user_model

User = get_user_model()

class VHMSProfileForm(ProfileForm):

    class Meta:
        model = User
        fields = ("email", "username")

    def __init__(self, *args, **kwargs):
        super(VHMSProfileForm, self).__init__(*args, **kwargs)
        self._signup = self.instance.id is None
        if not self._signup:
            self.fields["email"].widget.attrs['readonly'] = True
