from django.db import models
from django.utils.translation import ugettext_lazy as _
from os.path import splitext
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.db.models import signals


def upload_avatar_to(instance, filename):
    filename_base, filename_ext = splitext(filename)
    return 'profiles/%s%s' % (now().strftime("%Y%m%d%H%M%S"),filename_ext.lower(),)


class Profile(models.Model):
    """

    """
    user = models.OneToOneField(User, related_name='profile')
    is_merchant = models.BooleanField(default=False)
    profiletype = models.CharField(verbose_name=_("Profile Type"), max_length=2)
    avatar = models.ImageField(_("Avatar"), upload_to=upload_avatar_to, blank=True)
    about = models.CharField(verbose_name=_("About myself"), max_length=1024)
    city = models.CharField(verbose_name=_("City"), max_length=128)
    country = models.CharField(verbose_name=_("Country"), max_length=128)

    class Meta:
        verbose_name = _("Profile")

    def save(self, *args, **kwargs):
        # 1 - for local profile, 2 - for social accounts. mock.
        # { WORKAROUND: убрать статическую переменную}
        self.profiletype = 1
        super(Profile, self).save(*args, **kwargs)



def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

signals.post_save.connect(create_user_profile, sender=User)

