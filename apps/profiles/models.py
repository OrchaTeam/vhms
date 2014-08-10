from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class Profile(models.Model):

    first_name = models.CharField(verbose_name=_("First Name"), max_length=64)
    last_name = models.CharField(verbose_name=_("Second Name"), max_length=64)
    is_merchant = models.BooleanField(default=False)
    related_profile = models.ForeignKey("Profile", null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    profiletype = models.CharField(verbose_name=_("Profile Type"), max_length=2)

    class Meta:
        verbose_name = _("Profile")

    def __str__(self):
        return u"%s %s" % (self.first_name, self.last_name)

    def save(self, *args, **kwargs):
        # 1 - for local profile, 2 - for social accounts. this is mock. {WORKAROUND: убрать статическую переменную}
        self.profiletype = 1
        super(Profile, self).save(*args, **kwargs)
    