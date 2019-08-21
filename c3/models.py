from collections import OrderedDict
import time
from django.conf import settings as django_settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from magi.abstract_models import BaseAccount, AccountAsOwnerModel
from magi.django_translated import t
from magi.item_model import MagiModel, i_choices
from magi.models import uploadItem
from magi.utils import (
    AttrDict,
)
from c3.utils import getCachedCCC
from c3.c3_translations import ct

TRANSLATION_LANGUAGES = [ l for l in django_settings.LANGUAGES if l[0] != 'en' ]
TRANSLATION_LANGUAGES_EXCEPT_GERMAN = [ l for l in django_settings.LANGUAGES if l[0] not in ['de', 'en'] ]

############################################################
# Account = attended CCC
############################################################

class Account(BaseAccount):
    ccc = models.ForeignKey('CCC', related_name='attendances', verbose_name='CCC')

    m_description = models.TextField(ct['How was it?'], null=True)

    ############################################################
    # Views utils

    @property
    def cached_ccc(self):
        d = { 'id': self.id }
        d.update(getCachedCCC(self.ccc_id))
        return AttrDict(self.cached_json_extra('ccc', d))

    display_nickname = property(lambda _s: unicode(_s))

    ############################################################
    # Unicode

    def __unicode__(self):
        return ct['{username} went to {ccc}'].format(
            username=self.cached_owner.username,
            ccc=self.cached_ccc.get('name', 'CCC'),
        )

############################################################
# CCC
############################################################

class CCC(MagiModel):
    collection_name = 'ccc'
    owner = models.ForeignKey(User, related_name='added_ccc')

    image = models.ImageField(ct['Logo'], upload_to=uploadItem('ccc'), max_length=500)

    TYPE_CHOICES = [
        ('congress', ct['Congress']),
        ('camp', ct['Camp']),
    ]
    i_type = models.PositiveIntegerField(_('Type'), choices=i_choices(TYPE_CHOICES))

    name = models.CharField(_('Title'), max_length=100)
    NAMES_CHOICES = TRANSLATION_LANGUAGES
    d_names = models.TextField(_('Title'), null=True)

    number = models.PositiveIntegerField(_('Number'), null=True)

    start_date = models.DateTimeField(_('Start date'))
    end_date = models.DateTimeField(_('End'), null=True)

    main_url = models.URLField(_('Wiki'), null=True)

    m_description = models.TextField(_('Description'), null=True)
    M_DESCRIPTIONS_CHOICES = TRANSLATION_LANGUAGES
    d_m_descriptions = models.TextField(_('Description'), null=True)

    ############################################################
    # Reverse relations

    reverse_related = [
        { 'field_name': 'talks' },
    ]

    ############################################################
    # Views utils

    @property
    def year(self):
        return self.start_date.year if self.start_date else None

    @classmethod
    def get_acronym(self, type, number, year):
        if type == 'congress' and number:
            return u'{}c3'.format(number)
        elif type == 'camp' and year:
            return u'camp{}'.format(year)
        return None

    @property
    def acronym(self):
        return type(self).get_acronym(self.type, self.number, self.year)

    ############################################################
    # Unicode

    def __unicode__(self):
        return u' '.join([
            s for s in [
                self.acronym or '',
                self.name,
                u' ({})'.format(self.t_name) if self.t_name != self.name else '',
            ]  if s])

############################################################
# Hackerspace
############################################################

class Hackerspace(MagiModel):
    collection_name = 'hackerspace'
    owner = models.ForeignKey(User, related_name='added_hackerspace')

    image = models.ImageField(ct['Logo'], upload_to=uploadItem('hackerspaces'))

    name = models.CharField(_('Title'), max_length=100, null=True)

    address = models.TextField(null=True)

    m_description = models.TextField(_('Description'), null=True)
    M_DESCRIPTIONS_CHOICES = TRANSLATION_LANGUAGES
    d_m_descriptions = models.TextField(_('Description'), null=True)

    def __unicode__(self):
        return self.name

############################################################
# Talk
############################################################

class Talk(MagiModel):
    collection_name = 'talk'
    owner = models.ForeignKey(User, related_name='added_talk')
    ccc = models.ForeignKey('CCC', related_name='talks', verbose_name='CCC')

    fahrplan_guid = models.CharField('Fahrplan GUID', null=True, max_length=199)

    name = models.CharField(_('Title'), max_length=100)
    NAMES_CHOICES = TRANSLATION_LANGUAGES
    d_names = models.TextField(_('Title'), null=True)

    subtitle = models.CharField(ct['Subtitle'], max_length=100, null=True)
    SUBTITLES_CHOICES = TRANSLATION_LANGUAGES
    d_subtitles = models.TextField(ct['Subtitle'], null=True)

    description = models.TextField(_('Description'), null=True)
    DESCRIPTIONS_CHOICES = TRANSLATION_LANGUAGES
    d_descriptions = models.TextField(_('Description'), null=True)

    length = models.PositiveIntegerField(_('Length'), null=True)
    display_length = property(lambda _s: time.strftime(
        '%H:%M:%S' if _s.length >= 3600 else '%M:%S', time.gmtime(_s.length)))

    start_date = models.DateTimeField(_('Start date'))
    end_date = models.DateTimeField(_('End date'), null=True)

    image = models.ImageField(_('Image'), upload_to=uploadItem('talk'), null=True, max_length=500)

    url = models.URLField(_('About'), null=True)
    watch_url = models.URLField(ct['Watch'], null=True)

    LANGUAGE_CHOICES = OrderedDict([
        ('eng', _('English')),
        ('deu', _('German')),
        ('other', _('Other')),
    ])
    i_language = models.PositiveIntegerField(t['Language'], default=0, choices=i_choices(LANGUAGE_CHOICES))

    c_persons = models.TextField(ct['Persons'], null=True)
    c_tags = models.TextField(_('Tags'), null=True)

    ############################################################
    # Views utils

    @property
    def cached_ccc(self):
        d = { 'id': self.id }
        d.update(getCachedCCC(self.ccc_id))
        return AttrDict(self.cached_json_extra('ccc', d))

    def __unicode__(self):
        return self.name

class AttendedTalk(AccountAsOwnerModel):
    collection_name = 'attendedtalk'

    account = models.ForeignKey(Account, related_name='attended_talks')
    talk = models.ForeignKey(Talk, related_name='attended_talks', verbose_name=ct['Talk'])

    m_description = models.TextField(ct['How was it?'], null=True)

    image = property(lambda _s: _s.talk.image)
    image_url = property(lambda _s: _s.talk.image_url)
    http_image_url = property(lambda _s: _s.talk.http_image_url)

    def __unicode__(self):
        return unicode(self.talk)

    class Meta:
        unique_together = (('account', 'talk'), )

class WatchedTalk(MagiModel):
    collection_name = 'watchedtalk'

    owner = models.ForeignKey(User, related_name='watched_talks')
    talk = models.ForeignKey(Talk, related_name='watched_talks', verbose_name=ct['Talk'])

    m_description = models.TextField(ct['How was it?'], null=True)

    image = property(lambda _s: _s.talk.image)
    image_url = property(lambda _s: _s.talk.image_url)
    http_image_url = property(lambda _s: _s.talk.http_image_url)

    def __unicode__(self):
        return unicode(self.talk)

    class Meta:
        unique_together = (('owner', 'talk'), )

class WantToWatchTalk(MagiModel):
    collection_name = 'wanttowatchtalk'

    owner = models.ForeignKey(User, related_name='wanttowatch_talks')
    talk = models.ForeignKey(Talk, related_name='wanttowatch_talks', verbose_name=ct['Talk'])

    image = property(lambda _s: _s.talk.image)
    image_url = property(lambda _s: _s.talk.image_url)
    http_image_url = property(lambda _s: _s.talk.http_image_url)

    def __unicode__(self):
        return unicode(self.talk)

    class Meta:
        unique_together = (('owner', 'talk'), )

############################################################
# Session
############################################################

class Session(MagiModel):
    collection_name = 'session'
    owner = models.ForeignKey(User, related_name='added_session')

    TYPE_CHOICES = (
        ct['Assembly'],
        ct['Workshop'],
        ct['Party'],
        ct['Session'],
        _('Other'),
    )
    i_type = models.PositiveIntegerField(_('Type'), choices=i_choices(TYPE_CHOICES))

    name = models.CharField(_('Title'), max_length=100, null=True)

    # todo use github to convert?
    m_description = models.TextField(_('Description'), null=True)
    M_DESCRIPTIONS_CHOICES = TRANSLATION_LANGUAGES
    d_m_descriptions = models.TextField(_('Description'), null=True)

    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True)

    def __unicode__(self):
        return self.name

############################################################
# Question
############################################################

class Question(MagiModel):
    collection_name = 'question'
    owner = models.ForeignKey(User, related_name='added_question', verbose_name=ct['Asked by'])

    name = models.CharField(_('Question'), max_length=100)

    def __unicode__(self):
        return self.name

############################################################
# Project
############################################################

class Project(MagiModel):
    collection_name = 'project'
    owner = models.ForeignKey(User, related_name='added_project')

    image = models.ImageField(ct['Logo'], upload_to=uploadItem('project'))

    name = models.CharField(_('Title'), max_length=100)

    main_url = models.URLField(null=True)

    def __unicode__(self):
        return self.name

############################################################
# CCCLink
############################################################

class CCCLink(MagiModel):
    collection_name = 'link'
    ccc = models.ForeignKey(CCC, related_name='links')
    owner = property(lambda _s: _s.ccc.owner)
    owner_id = property(lambda _s: _s.ccc.owner_id)

    name = models.CharField(_('Title'), max_length=100)
    NAMES_CHOICES = TRANSLATION_LANGUAGES
    d_names = models.TextField(_('Title'), null=True)

    url = models.URLField(null=True)

    def __unicode__(self):
        return self.name

############################################################
# Link
############################################################

class Link(MagiModel):
    collection_name = 'link'
    owner = models.ForeignKey(User, related_name='added_link')

    name = models.CharField(_('Title'), max_length=100)
    NAMES_CHOICES = TRANSLATION_LANGUAGES
    d_names = models.TextField(_('Title'), null=True)

    in_navbar = models.BooleanField(default=False)

    url = models.URLField(null=True)

    ############################################################
    # Views utils

    display_item_url = property(lambda _s: _s.url)

    ############################################################
    # Unicode

    def __unicode__(self):
        return self.name

############################################################
# Photo
############################################################

class Photo(AccountAsOwnerModel):
    collection_name = 'photo'

    image = models.ImageField(ct['Logo'], upload_to=uploadItem('ccc'))

    name = models.CharField(_('Title'), max_length=100, null=True)

    def __unicode__(self):
        return self.name
