from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class ProfileType(models.Model):

    name = models.CharField(verbose_name=_("profile_type"), max_length=2)

    class Meta:
        verbose_name = _("ProfileType")

    def __str__(self):
        return u"%s" % (self.name)

class Profile(models.Model):

    first_name = models.CharField(verbose_name=_("irst_name"), max_length=64)
    last_name = models.CharField(verbose_name=_("second_name"), max_length=64)
    birthday = models.DateTimeField(verbose_name=_("birthday"), null=True)
    is_merchant = models.BooleanField(default=False)
    related_profile = models.ForeignKey("Profile", null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    type = models.ForeignKey("ProfileType")

    class Meta:
        verbose_name = _("Profile")

    def __str__(self):
        return u"%s %s" % (self.first_name, self.last_name)
