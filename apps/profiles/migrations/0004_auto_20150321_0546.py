# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20150321_0458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='city',
            field=models.CharField(verbose_name='City', max_length=128, blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='country',
            field=models.CharField(verbose_name='Country', max_length=128, blank=True),
        ),
    ]
