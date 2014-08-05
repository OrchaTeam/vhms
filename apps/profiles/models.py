from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class Profile(models.Model):

    first_name = models.CharField(verbose_name=_("first_name"), max_length=64)
    last_name = models.CharField(verbose_name=_("second_name"), max_length=64)
    is_merchant = models.BooleanField(default=False)
    related_profile = models.ForeignKey("Profile", null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        verbose_name = _("Profile")

    def __str__(self):
        return u"%s %s" % (self.first_name, self.last_name)

    