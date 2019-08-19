from __future__ import print_function
import datetime
from pprint import pprint
from dateutil.relativedelta import relativedelta
from django.utils.dateparse import parse_datetime
from magi.import_data import api_pages, import_data as magi_import_data
from magi.tools import get_default_owner
from c3 import models
from c3 import raw

def importSchedule(local, log_function, verbose, year, ccc):
    if year not in raw.SCHEDULES:
        return

    def before_importing_schedule(result):
        ccc.start_date = result['schedule']['conference']['start']
        ccc.end_date = result['schedule']['conference']['end']
        ccc.save()
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
        url=raw.SCHEDULES[year],
        name=u'talks-{}'.format(year),
        details={
            'callback_before_page': before_importing_schedule,
            'model': models.Talk,
            'endpoint': '',
            'unique_fields': [
                'fahrplan_id',
            ],
            'mapping': {
                'id': 'fahrplan_id',
                'date': lambda v: ('start_date', parse_datetime(v)),
                'title': 'name',
                'logo': lambda v: (
                    'image',
                    u'https://fahrplan.events.ccc.de/congress/{}/Fahrplan{}'.format(year, v) if v else None,
                ),
            },
            'ignored_fields': [
                'subtitle', 'room', 'language', 'persons',
                'track', 'type', 'abstract', 'attachments', 'slug',
                'guid', 'do_not_record', 'start',
                'recording_license', 'description', 'links',
                # used in callback
                'duration',
            ],
            'callback': callback,
        },
        local=local,
        log_function=log_function,
        verbose=verbose,
    )

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
    return
    # Media API, todo
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
                    'number',
                    'year',
                ],
                'unique_together': True,
                'mapping': {
                    'acronym': lambda value: {
                        'number': int(value[:-2]) if value.endswith('c3') else None,
                        'i_type': 'congress' if value.endswith('c3') else 'camp',
                    },
                    'logo_url': 'image',
                    # 'url': '',
                },
                'ignored_fields': [
                    'aspect_ratio', 'updated_at', 'title', 'slug',
                    'event_last_released_at', 'webgen_location',
                    'schedule_url',
                ],
            },
        },
        local=local,
        to_import=to_import,
        log_function=log_function,
        verbose=verbose,
    )
