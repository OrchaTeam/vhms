from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from os.path import splitext
from django.utils.timezone import now

def upload_avatar_to(instance, filename):
    filename_base, filename_ext = splitext(filename)
    return 'profiles/%s%s' % (now().strftime("%Y%m%d%H%M%S"),filename_ext.lower(),)

class Profile(models.Model):

    first_name = models.CharField(verbose_name=_("First Name"), max_length=64)
    last_name = models.CharField(verbose_name=_("Second Name"), max_length=64)
    is_merchant = models.BooleanField(default=False)
    related_profile = models.ForeignKey("Profile", null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    profiletype = models.CharField(verbose_name=_("Profile Type"), max_length=2)
    avatar = models.ImageField(_("Avatar"), upload_to=upload_avatar_to, blank=True)

    class Meta:
        verbose_name = _("Profile")

    def __str__(self):
        return u"%s %s" % (self.first_name, self.last_name)

    def save(self, *args, **kwargs):
        # 1 - for local profile, 2 - for social accounts. mock. { WORKAROUND: убрать статическую переменную}
        self.profiletype = 1
        super(Profile, self).save(*args, **kwargs)