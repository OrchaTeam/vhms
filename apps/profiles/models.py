from django.db import models
from django.utils.translation import ugettext_lazy as _
from os.path import splitext
from django.utils.timezone import now
from django.contrib.auth.models import User, UserManager

def upload_avatar_to(instance, filename):
    filename_base, filename_ext = splitext(filename)
    return 'profiles/%s%s' % (now().strftime("%Y%m%d%H%M%S"),filename_ext.lower(),)

class Profile(User):

    is_merchant = models.BooleanField(default=False)
    profiletype = models.CharField(verbose_name=_("Profile Type"), max_length=2)
    avatar = models.ImageField(_("Avatar"), upload_to=upload_avatar_to, blank=True)
    objects = UserManager()

    class Meta:
        verbose_name = _("Profile")

    def __str__(self):
        return u"%s %s" % (self.first_name, self.last_name)

    def save(self, *args, **kwargs):
        # 1 - for local profile, 2 - for social accounts. mock.
        # { WORKAROUND: убрать статическую переменную}
        self.profiletype = 1
        super(Profile, self).save(*args, **kwargs)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """

        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()