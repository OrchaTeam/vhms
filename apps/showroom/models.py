from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class Item(models.Model):

    # user input
    name = models.CharField(verbose_name=_("Item Name"),
                            max_length=128)
    descr = models.CharField(verbose_name=_("Item Description"),
                             max_length=256)
    cost = models.FloatField(verbose_name=_("Item Cost"),
                             blank=True)
    material = models.CharField(verbose_name=_("Item Material"),
                                max_length=128,
                                blank=True)
    dimensions = models.CharField(verbose_name=_("Dimensions"),
                                  max_length=32,
                                  blank=True)
    weight = models.FloatField(verbose_name=_("Weight"),
                               blank=True)
    tag_id = models.ManyToManyField('Tag',
                                    verbose_name=_("Tag"),
                                    blank=True)
    groupitem_id = models.ForeignKey('GroupItem', verbose_name=_("Group"))

    # auto input
    created_at = models.DateField(verbose_name=_("Created at"),)
    changed_at = models.DateField(verbose_name=_("Changed at"))
    author_id = models.ForeignKey(User,
                                  verbose_name=_("Author"),
                                  related_name="+")

    class Meta:
        verbose_name = _("Item")

    def __unicode__(self):
        return self.name


class GroupItem(models.Model):

    name = models.CharField(verbose_name=_("Group Name"),
                            max_length=64)
    descr = models.CharField(verbose_name=_("Group Description"),
                             max_length=256)

    class Meta:
        verbose_name = _("Group Item")

    def __unicode__(self):
        return self.name

class Tag(models.Model):

    name = models.CharField(verbose_name=_("Item Name"),
                            max_length=128)
    author_id = models.ForeignKey(User, verbose_name=_("Author"))
    created_at = models.DateField(verbose_name=_("Created at"))
    descr = models.CharField(verbose_name=_("Tag Description"),
                             blank=True,
                             max_length=128)

    class Meta:
        verbose_name = _("Tag")

    def __unicode__(self):
        return self.name