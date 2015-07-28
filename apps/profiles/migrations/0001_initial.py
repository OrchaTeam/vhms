# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.profiles.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('is_merchant', models.BooleanField(default=False)),
                ('profiletype', models.CharField(max_length=2, verbose_name='Profile Type')),
                ('first_name', models.CharField(max_length=64, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=64, verbose_name='Last Name')),
                ('avatar', models.ImageField(upload_to=apps.profiles.models.upload_avatar_to, blank=True, verbose_name='Avatar')),
                ('about', models.CharField(max_length=1024, verbose_name='About myself')),
                ('city', models.CharField(max_length=128, verbose_name='City')),
                ('country', models.CharField(max_length=128, verbose_name='Country')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='profile')),
            ],
            options={
                'verbose_name': 'Profile',
            },
            bases=(models.Model,),
        ),
    ]
