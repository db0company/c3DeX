# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import magi.utils


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_cache_owner_last_update', models.DateTimeField(null=True)),
                ('_cache_owner_username', models.CharField(max_length=32, null=True)),
                ('_cache_owner_email', models.EmailField(max_length=75, blank=True)),
                ('_cache_owner_preferences_i_status', models.CharField(max_length=12, null=True)),
                ('_cache_owner_preferences_twitter', models.CharField(max_length=32, null=True, blank=True)),
                ('_cache_owner_color', models.CharField(max_length=100, null=True, blank=True)),
                ('creation', models.DateTimeField(auto_now_add=True, verbose_name='Join date')),
                ('nickname', models.CharField(help_text="Give a nickname to your account to easily differentiate it from your other accounts when you're managing them.", max_length=200, null=True, verbose_name='Nickname')),
                ('start_date', models.DateField(null=True, verbose_name='Start date')),
                ('level', models.PositiveIntegerField(null=True, verbose_name='Level')),
                ('default_tab', models.CharField(max_length=100, null=True, verbose_name='Default tab')),
                ('_cache_leaderboards_last_update', models.DateTimeField(null=True)),
                ('_cache_leaderboard', models.PositiveIntegerField(null=True)),
                ('m_description', models.TextField(null=True, verbose_name='How was it?')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AttendedTalk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_cache_account_last_update', models.DateTimeField(null=True)),
                ('_cache_j_account', models.TextField(null=True)),
                ('m_description', models.TextField(null=True, verbose_name='How was it?')),
                ('account', models.ForeignKey(related_name='attended_talks', to='c3.Account')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CCC',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=magi.utils.uploadItem(b'ccc'), verbose_name='Logo')),
                ('i_type', models.PositiveIntegerField(verbose_name='Type', choices=[(0, 'Congress'), (1, 'Camp')])),
                ('name', models.CharField(max_length=100, verbose_name='Title')),
                ('d_names', models.TextField(null=True, verbose_name='Title')),
                ('number', models.PositiveIntegerField(null=True, verbose_name='Number')),
                ('start_date', models.DateTimeField(verbose_name='Start date')),
                ('end_date', models.DateTimeField(null=True, verbose_name='End')),
                ('main_url', models.URLField(null=True, verbose_name='Wiki')),
                ('m_description', models.TextField(null=True, verbose_name='Description')),
                ('d_m_descriptions', models.TextField(null=True, verbose_name='Description')),
                ('owner', models.ForeignKey(related_name='added_ccc', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CCCLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='Title')),
                ('d_names', models.TextField(null=True, verbose_name='Title')),
                ('url', models.URLField(null=True)),
                ('ccc', models.ForeignKey(related_name='links', to='c3.CCC')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Hackerspace',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=magi.utils.uploadItem(b'hackerspaces'), verbose_name='Logo')),
                ('name', models.CharField(max_length=100, null=True, verbose_name='Title')),
                ('address', models.TextField(null=True)),
                ('m_description', models.TextField(null=True, verbose_name='Description')),
                ('d_m_descriptions', models.TextField(null=True, verbose_name='Description')),
                ('owner', models.ForeignKey(related_name='added_hackerspace', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='Title')),
                ('d_names', models.TextField(null=True, verbose_name='Title')),
                ('in_navbar', models.BooleanField(default=False)),
                ('url', models.URLField(null=True)),
                ('owner', models.ForeignKey(related_name='added_link', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_cache_account_last_update', models.DateTimeField(null=True)),
                ('_cache_j_account', models.TextField(null=True)),
                ('image', models.ImageField(upload_to=magi.utils.uploadItem(b'ccc'), verbose_name='Logo')),
                ('name', models.CharField(max_length=100, null=True, verbose_name='Title')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=magi.utils.uploadItem(b'project'), verbose_name='Logo')),
                ('name', models.CharField(max_length=100, verbose_name='Title')),
                ('main_url', models.URLField(null=True)),
                ('owner', models.ForeignKey(related_name='added_project', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='Question')),
                ('owner', models.ForeignKey(related_name='added_question', verbose_name='Asked by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('i_type', models.PositiveIntegerField(verbose_name='Type', choices=[(0, 'Assembly'), (1, 'Workshop'), (2, 'Party'), (3, 'Session'), (4, 'Other')])),
                ('name', models.CharField(max_length=100, null=True, verbose_name='Title')),
                ('m_description', models.TextField(null=True, verbose_name='Description')),
                ('d_m_descriptions', models.TextField(null=True, verbose_name='Description')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField(null=True)),
                ('owner', models.ForeignKey(related_name='added_session', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Talk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fahrplan_id', models.PositiveIntegerField(null=True)),
                ('name', models.CharField(max_length=100, verbose_name='Title')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField(null=True)),
                ('image', models.ImageField(upload_to=magi.utils.uploadItem(b'talk'), null=True, verbose_name='Image')),
                ('ccc', models.ForeignKey(related_name='talks', verbose_name=b'CCC', to='c3.CCC')),
                ('owner', models.ForeignKey(related_name='added_talk', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WantToWatchTalk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('owner', models.ForeignKey(related_name='wanttowatch_talks', to=settings.AUTH_USER_MODEL)),
                ('talk', models.ForeignKey(related_name='wanttowatch_talks', verbose_name='Talk', to='c3.Talk')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WatchedTalk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('m_description', models.TextField(null=True, verbose_name='How was it?')),
                ('owner', models.ForeignKey(related_name='watched_talks', to=settings.AUTH_USER_MODEL)),
                ('talk', models.ForeignKey(related_name='watched_talks', verbose_name='Talk', to='c3.Talk')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='watchedtalk',
            unique_together=set([('owner', 'talk')]),
        ),
        migrations.AlterUniqueTogether(
            name='wanttowatchtalk',
            unique_together=set([('owner', 'talk')]),
        ),
        migrations.AddField(
            model_name='attendedtalk',
            name='talk',
            field=models.ForeignKey(related_name='attended_talks', verbose_name='Talk', to='c3.Talk'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='attendedtalk',
            unique_together=set([('account', 'talk')]),
        ),
        migrations.AddField(
            model_name='account',
            name='ccc',
            field=models.ForeignKey(related_name='attendances', verbose_name=b'CCC', to='c3.CCC'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='owner',
            field=models.ForeignKey(related_name='accounts', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
