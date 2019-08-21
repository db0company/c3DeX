import datetime
from collections import OrderedDict
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings as django_settings
from django.utils import timezone
from magi.tools import (
    getStaffConfigurations,
    generateSettings,
    getUsersBirthdaysToday,
)
from magi import urls # unused, needed to load RAW_CONTEXT
from magi.utils import (
    getAllTranslationsOfModelField,
    getCurrentEvents,
    staticImageURL,
    getAllTranslations,
)
from c3 import models

def generate_settings():

    print 'Get staff configurations and latest news'
    staff_configurations, latest_news = getStaffConfigurations()

    print 'Show a happy birthday banner for the users whose birthday is today'
    latest_news = getUsersBirthdaysToday(
        staticImageURL('happy_birthday.png'),
        latest_news=latest_news,
        max_usernames=4,
    )

    print 'Cache all CCCs'
    all_cccs = OrderedDict([
        (ccc.id, {
            'name': unicode(ccc),
            't_names': getAllTranslations(lambda _language: ccc, unique=True),
            'image_url': ccc.image_url,
            'acronym': ccc.acronym,
        }) for ccc in models.CCC.objects.all().order_by('-start_date')
    ])

    print 'Links in navbar'
    links_in_navbar = OrderedDict([
        (link.id, {
            'name': unicode(link),
            't_names': getAllTranslations(lambda _language: link, unique=True),
            'url': link.url,
        }) for link in models.Link.objects.filter(in_navbar=True).order_by('id')
    ])

    print 'Add CCC to latest news'
    recent_cccs = getCurrentEvents(models.CCC.objects.all(), starts_within=1360, ends_within=1360)
    # todo not working
    latest_news += [{
        't_titles': getAllTranslations(lambda _language: item),
        'image': ccc.image_url,
        'url': ccc.item_url,
    } for ccc in recent_cccs]

    print 'Save generated settings'
    generateSettings({
        'LATEST_NEWS': latest_news,
        'STAFF_CONFIGURATIONS': staff_configurations,
        'CCCS': all_cccs,
        'LINKS_IN_NAVBAR': links_in_navbar,
    }, imports=[
        'from collections import OrderedDict',
    ])

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        generate_settings()
