# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupItem',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=64, verbose_name='Group Name')),
                ('descr', models.CharField(max_length=256, verbose_name='Group Description')),
            ],
            options={
                'verbose_name': 'Group Item',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=128, verbose_name='Item Name')),
                ('descr', models.CharField(max_length=256, verbose_name='Item Description')),
                ('cost', models.FloatField(verbose_name='Item Cost', blank=True)),
                ('material', models.CharField(max_length=128, verbose_name='Item Material', blank=True)),
                ('dimensions', models.CharField(max_length=32, verbose_name='Dimensions', blank=True)),
                ('weight', models.FloatField(verbose_name='Weight', blank=True)),
                ('created_at', models.DateField(verbose_name='Created at')),
                ('changed_at', models.DateField(verbose_name='Changed at')),
                ('author_id', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('groupitem_id', models.ForeignKey(to='showroom.GroupItem', verbose_name='Group')),
            ],
            options={
                'verbose_name': 'Item',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=128, verbose_name='Item Name')),
                ('created_at', models.DateField(verbose_name='Created at')),
                ('descr', models.CharField(max_length=128, verbose_name='Tag Description', blank=True)),
                ('author_id', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Author')),
            ],
            options={
                'verbose_name': 'Tag',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='item',
            name='tag_id',
            field=models.ManyToManyField(to='showroom.Tag', verbose_name='Tag', blank=True),
            preserve_default=True,
        ),
    ]
