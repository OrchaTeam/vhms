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
    first_name = models.CharField(verbose_name=_("First Name"), max_length=64)
    last_name = models.CharField(verbose_name=("Last Name"), max_length=64)
    avatar = models.ImageField(_("Avatar"), upload_to=upload_avatar_to, blank=True)
    about = models.CharField(verbose_name=_("About myself"), max_length=1024)
    city = models.CharField(verbose_name=_("City"), max_length=128, blank=True)
    country = models.CharField(verbose_name=_("Country"), max_length=128, blank=True)

    class Meta:
        verbose_name = _("Profile")


# local -
def create_profile_from_local(sender, instance, created, **kwargs):
    """
    It's the method for creating a profile
    instance after a local registration.
    It's launched by a signal.
    """
    if created:
        Profile.objects.get_or_create(
            user=instance,
            defaults={
                "first_name": instance.first_name,
                "last_name": instance.last_name,
                "profiletype": 1})


# signal from local registration
signals.post_save.connect(create_profile_from_local, sender=User)