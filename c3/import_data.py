from __future__ import print_function
import datetime
from pprint import pprint
from dateutil.relativedelta import relativedelta
from django.utils.dateparse import parse_datetime
from magi.import_data import api_pages, import_data as magi_import_data
from magi.tools import get_default_owner
from c3 import models, raw, settings
from c3.utils import (
    getCCCHashtag,
)

def importSchedule(local, log_function, verbose, year, ccc, type='congress'):
    if year not in (raw.SCHEDULES if type == 'congress' else raw.CAMP_SCHEDULES):
        return
    print(ccc)

    def before_importing_schedule(result):
        ccc.start_date = result['schedule']['conference']['start']
        ccc.end_date = result['schedule']['conference']['end']
        ccc.save()
        _ccc = models.CCC.objects.get(id=ccc.id)
        ccc.start_date = _ccc.start_date
        ccc.end_date = _ccc.end_date
        talks = []
        for day in result['schedule']['conference']['days']:
            for room_schedule in day['rooms'].values():
                for talk in room_schedule:
                    talks.append(talk)
        return talks

    def callback(details, item, unique_data, data):
        data['ccc'] = ccc
        if 'start_date' in data:
            data['end_date'] = data['start_date'] + relativedelta(
                hours=int(item['duration'].split(':')[0]),
                minutes=int(item['duration'].split(':')[1]),
            )

    api_pages(
        url=(raw.SCHEDULES if type == 'congress' else raw.CAMP_SCHEDULES)[year],
        name=u'talks-{}'.format(year),
        details={
            'callback_before_page': before_importing_schedule,
            'model': models.Talk,
            'endpoint': '',
            'unique_fields': [
                'fahrplan_guid',
            ],
            'mapping': {
                'guid': 'fahrplan_guid',
                'date': lambda v: ('start_date', parse_datetime(v)),
                'title': lambda v: ('name', v[100:]),
                'logo': lambda v: (
                    'image',
                    u'https://fahrplan.events.ccc.de/congress/{}/Fahrplan{}'.format(year, v) if v else None,
                ),
            },
            'ignored_fields': [
                'subtitle', 'room', 'language', 'persons',
                'track', 'type', 'abstract', 'attachments', 'slug',
                'do_not_record', 'start',
                'recording_license', 'description', 'links',
                # used in callback
                'duration',
            ],
            'callback': callback,
            'mapped_fields': [
                'fahrplan_guid', 'start_date', 'name',
                'logo',
            ],
            'dont_erase_existing_value_fields': [
                'name', 'logo',
            ],
        },
        local=local,
        log_function=log_function,
        verbose=verbose,
    )

def mediaAPICallbackAfterSavedCCC(local, log_function, verbose):
    def _lambda(details, item, json_item):
        ccc = models.CCC.objects.get(id=item.id)
        def callbackAddMedia(details, item, unique_data, data):
            data['ccc_id'] = ccc.id
            if not data.get('start_date', None):
                if item.get('release_date', None):
                    data['start_date'] = item['release_date']
                else:
                    data['start_date'] = ccc['start_date']
        if ccc.type == 'camp' and ccc.year in raw.CAMP_SCHEDULES:
            importSchedule(local, log_function, verbose, ccc.year, ccc)
        api_pages(
            url=json_item['url'],
            name=u'media-talks-{}'.format(ccc.year),
            details={
                'model': models.Talk,
                'results_location': ['events'],
                'endpoint': '',
                'unique_fields': [
                    'fahrplan_guid',
                ],
                'fields': [
                    'description', 'length',
                ],
                'mapping': {
                    'guid': 'fahrplan_guid',
                    'subtitle': lambda v: ('subtitle', v[100:] if v else None),
                    'link': 'url',
                    'title': lambda v: ('name', v[100:]),
                    'original_language': 'i_language',
                    'persons': 'c_persons',
                    'tags': lambda v: ('c_tags', [_t for _t in [
                        getCCCHashtag(tags=settings.ACTIVITY_TAGS, acronym=_t)
                        or (_t if _t in dict(settings.ACTIVITY_TAGS).keys() else None)
                        for _t in v
                    ] if _t]),
                    'date': lambda v: ('start_date', parse_datetime(v) if v else None),
                    'thumb_url': 'image',
                    'frontend_link': 'watch_url',
                },
                'callback': callbackAddMedia,
                'ignored_fields': [
                    'slug', 'view_count', 'promoted',
                    'release_date', 'updated_at', 'duration',
                    'poster_url', 'timeline_url', 'thumbnails_url',
                    'url', 'conference_url', 'related'
                ],
                'dont_erase_existing_value_fields': [
                    'start_date', 'name', 'c_persons', 'c_tags',
                    'image', 'subtitle', 'description', 'length',
                ],
            },
            local=local,
            log_function=log_function,
            verbose=verbose,
        )
    return _lambda

def import_data(local=False, to_import=None, log_function=print, verbose=False):
    default_owner = get_default_owner()
    number = 1

    # Schedule JSON
    if not to_import or 'congresses' in to_import or 'schedule' in to_import:
        for year, name in raw.CCCS.items():
            ccc, created = models.CCC.objects.get_or_create(name=name, defaults={
                'owner': default_owner,
                'i_type': models.CCC.get_i('type', 'congress'),
                'number': number,
                'start_date': u'{}-01-01'.format(year),
                'main_url': u'https://events.ccc.de/congress/{}/'.format(year),
            })
            if not to_import or 'schedule' in to_import:
                importSchedule(local, log_function, verbose, year, ccc)
            number += 1

    def findExistingCCC(model, unique_data, data, manytomany, dictionaries):
        if unique_data['i_type'] == 1: # camp
            year = unique_data['number']
            unique_data['number'] = None
            try:
                item = model.objects.filter(i_type=1, start_date__year=year)[0]
            except IndexError:
                item = None
        else:
            # congress
            try:
                item = model.objects.filter(i_type=0, number=unique_data['number'])[0]
            except IndexError:
                item = None
        if item and item.start_date and 'start_date' in data:
           del(data['start_date'])
        return item

    # Media API
    magi_import_data(
        url=raw.MEDIA_API_URL,
        import_configuration={
            'congresses': {
                'model': models.CCC,
                'results_location': ['conferences'],
                'endpoint': 'conferences',
                'callback_should_import': lambda _details, item: (
                    item['acronym'].endswith('c3') or item['acronym'].startswith('camp')),
                'unique_fields': [
                    'i_type',
                    'number',
                ],
                'find_existing_item': findExistingCCC,
                'mapping': {
                    'acronym': lambda value: {
                        'number': int(value[:-2]) if value.endswith('c3') else int(value[4:]),
                        'i_type': 'congress' if value.endswith('c3') else 'camp',
                    },
                    'logo_url': 'image',
                    'event_last_released_at': 'start_date',
                },
                'ignored_fields': [
                    'aspect_ratio', 'updated_at', 'title', 'slug',
                    'webgen_location', 'schedule_url',
                ],
                'callback_after_save': mediaAPICallbackAfterSavedCCC(local, log_function, verbose),
            },
        },
        local=local,
        to_import=to_import,
        log_function=log_function,
        verbose=verbose,
    )
